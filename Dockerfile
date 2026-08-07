# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modifications Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.

# To build with a different base image
# please run `./runtests.sh --clean && DOCKER_BUILDKIT=1 docker build -t projectmonai/monailabel:latest .`
# to use different version of MONAI pass `--build-arg FINAL_IMAGE=...`
#
# AMD ROCm build (default): torch comes from the ROCm wheel index and MONAI is
# provided by amd-monai (with amd-hipcim) from the AMD ROCm pip index. Override the ROCm base / indices
# with the build-args below, e.g.:
#   DOCKER_BUILDKIT=1 docker build \
#     --build-arg FINAL_IMAGE=rocm/dev-ubuntu-24.04:7.2-complete \
#     --build-arg TORCH_INDEX_URL=https://download.pytorch.org/whl/rocm7.1 \
#     --build-arg AMDGPU_TARGETS=gfx942 -t amd-monailabel:latest .
ARG FINAL_IMAGE=rocm/dev-ubuntu-24.04:7.2-complete
ARG BUILD_IMAGE=python:3.10
ARG NODE_IMAGE=node:slim
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/rocm7.1
ARG AMDGPU_TARGETS=gfx942

# Phase1: Build OHIF Viewer
FROM ${NODE_IMAGE} AS ohifbuild
COPY plugins/ohifv3 /opt/ohifv3
# node:slim ships only npm (no git/curl/yarn). Install git/curl and yarn (classic)
# up front so the viewer's requirements.sh finds yarn already present and skips
# its (broken) apt-based yarn install.
RUN apt update -y && apt install -y --no-install-recommends git curl ca-certificates && \
    npm install -g yarn
RUN cd /opt/ohifv3 && ./build.sh /opt/ohifv3/release
# Fail early if the viewer build produced no output (otherwise the COPY below
# fails much later with a confusing "file does not exist").
RUN test -d /opt/ohifv3/release && [ -n "$(ls -A /opt/ohifv3/release)" ] || \
    { echo "ERROR: OHIF build produced no /opt/ohifv3/release output"; exit 1; }

# Phase2: Build MONAI Label Package
FROM ${BUILD_IMAGE} AS build
ARG TORCH_INDEX_URL
WORKDIR /opt/monailabel
RUN python -m pip install pip setuptools wheel twine

RUN python -m pip install --no-cache-dir ninja && \
    python -m pip install --no-cache-dir torch --index-url ${TORCH_INDEX_URL}
ADD . /opt/monailabel/
COPY --from=ohifbuild /opt/ohifv3/release /opt/monailabel/monailabel/endpoints/static/ohif
# Build the wheel. .git is included in the context so versioneer resolves the
# real version (e.g. 0.8.5...). Drop --build-number so no date suffix is added,
# then rename the wheel to a clean, stable name: monailabel-<version>-py3.whl.
RUN BUILD_OHIF=false python setup.py bdist_wheel && \
    cd dist && \
    orig="$(ls monailabel-*.whl | head -1)" && \
    ver="$(echo "${orig}" | sed -E 's/^monailabel-([^+-]+).*/\1/')" && \
    mv "${orig}" "monailabel-${ver}-py3-none-any.whl" && \
    ls -l

# Phase3: Build Final Docker (AMD ROCm)
FROM ${FINAL_IMAGE}
LABEL maintainer="monai.contact@gmail.com"
WORKDIR /opt/monailabel

ARG TORCH_INDEX_URL
ARG AMDGPU_TARGETS
ENV ROCM_HOME=/opt/rocm \
    ROCM_PATH=/opt/rocm \
    HIP_PATH=/opt/rocm \
    PATH=/opt/rocm/bin:${PATH} \
    LD_LIBRARY_PATH=/opt/rocm/lib:${LD_LIBRARY_PATH} \
    AMDGPU_TARGETS=${AMDGPU_TARGETS} \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt /opt/monailabel/requirements.txt
COPY amd-constraints.txt /opt/monailabel/amd-constraints.txt

RUN apt update -y && apt install -y git curl openslide-tools python3 python-is-python3 python3-pip python3-setuptools python3-wheel
# Do NOT `pip install --upgrade pip`/wheel here: the base image ships them via
# Debian (no RECORD file), so uninstalling to upgrade fails. The distro pip/wheel
# are fine as-is; only ensure setuptools is >=61 (installs alongside, no removal).
RUN python -m pip install --no-cache-dir --upgrade "setuptools>=61"

# torch from the ROCm wheel index 
RUN python -m pip install --no-cache-dir torch torchvision torchaudio --index-url ${TORCH_INDEX_URL}

# amd-hipcim + amd-monai (MONAI's ROCm build) from the AMD ROCm pip index
RUN ROCM_VERSION="$(cat /opt/rocm/.info/version)" && \
    AMD_INDEX="https://pypi.amd.com/rocm-${ROCM_VERSION}/simple" && \
    python -m pip install --no-cache-dir amd-hipcim --extra-index-url="${AMD_INDEX}/" && \
    python -m pip install --no-cache-dir amd-monai --extra-index-url="${AMD_INDEX}"

# girder-client==3.2.3 ships only an sdist; under build isolation its build pulls
# setuptools_scm 10.x, which needs a `vcs_versioning` module that isn't available
# and fails metadata generation. Pre-install compatible build tooling and build
# girder-client with --no-build-isolation so it uses them.
RUN python -m pip install --no-cache-dir "setuptools-scm<8" "setuptools>=61" wheel && \
    python -m pip install --no-cache-dir --no-build-isolation girder-client==3.2.3

# SAM-2 (a git dependency) hangs under pip build-isolation because its isolated
# build env re-downloads torch from PyPI; torch is already installed above, so
# install everything else first, then SAM-2 with --no-build-isolation. girder-client
# is already installed above, so drop it from the bulk install too.
RUN SAM2_URL="$(grep -iE 'sam2\.git' requirements.txt | sed -E 's/^[^@]*@ *//; s/ *;.*$//' | head -1)" && \
    grep -ivE 'sam2\.git|^girder-client' requirements.txt > /tmp/req_nosam.txt && \
    python -m pip install --no-cache-dir -r /tmp/req_nosam.txt -c amd-constraints.txt && \
    if [ -n "${SAM2_URL}" ]; then \
        echo "Installing SAM-2 with --no-build-isolation: ${SAM2_URL}" && \
        python -m pip install --no-cache-dir --no-build-isolation "${SAM2_URL}"; \
    fi

# Install the MONAILabel wheel (deps already satisfied above)
COPY --from=build /opt/monailabel/dist/monailabel* /opt/monailabel/dist/
RUN python -m pip install -v --no-cache-dir --no-deps /opt/monailabel/dist/monailabel*.whl
