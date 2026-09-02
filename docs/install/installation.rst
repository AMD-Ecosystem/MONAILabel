.. SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

.. meta::
  :description: Install MONAILabel on ROCm from AMD PyPI, from source, or with Docker, on AMD Instinct GPUs
  :keywords: ROCm-LS, life sciences, MONAILabel installation, MONAILabel on ROCm

.. _installing-monailabel:

************************************
Installing MONAILabel on ROCm
************************************

Install MONAILabel on ROCm from :ref:`AMD PyPI <install-package>`, :ref:`from source <source-build>`, or with Docker.

These combinations are the install baseline.

.. list-table::
  :header-rows: 1
  :widths: 22 22 22 34

  * - ROCm version
    - Ubuntu version
    - Python version
    - AMD Instinct GPU
  * - 10.0.0
    - 24.04
    - 3.12
    - MI300X, MI325X, MI355X

PyTorch 2.13.0+rocm7.1, or a compatible ROCm PyTorch build, is required.

Setting up the environment
============================

Create a virtual environment and set ROCm environment variables before you install.

1. For an isolated environment, start an Ubuntu 24.04 Docker container with the ROCm base image.

   .. code:: shell

      docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true \
          --shm-size=128GB --network=host --device=/dev/kfd \
          --device=/dev/dri --group-add video -it \
          rocm/dev-ubuntu-24.04:7.15-complete

2. Create and activate a Python virtual environment.

   .. code:: shell

      python3 -m venv monailabel_env
      source monailabel_env/bin/activate
      pip install --upgrade pip

3. Set the environment variables. Set ``AMDGPU_TARGETS`` to the GFX target for
   your GPU. Use only one value. Use ``gfx942`` for MI300X and MI325X.
   Use ``gfx950`` for MI355X.

   .. code:: shell

      export ROCM_HOME=/opt/rocm
      export ROCM_PATH=/opt/rocm
      export HIP_PATH=/opt/rocm
      export HIP_VISIBLE_DEVICES=0
      export AMDGPU_TARGETS=gfx942
      # export AMDGPU_TARGETS=gfx950

.. _install-package:

Installing MONAILabel using AMD PyPI
======================================

If you don't intend to develop the library, install the ``amd-monailabel`` package.
Install the ROCm-validated ``amd-monai`` dependency from AMD PyPI first.
Then install ``amd-monailabel``.
Install PyTorch for ROCm before any other package that might pull a CUDA build.

1. Install the ROCm-validated MONAI build, ``amd-monai``, from AMD PyPI.

   .. code:: shell

      pip install "amd-monai==1.6.0" \
          --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

2. Install PyTorch for ROCm.

   .. code:: shell

      pip install --no-cache-dir torch torchvision torchaudio \
          --index-url https://download.pytorch.org/whl/rocm7.1

3. Install ``amd-monailabel`` without its dependencies.

   .. code:: shell

      pip install --no-cache-dir --no-deps amd-monailabel \
          --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

4. Install SAM-2, reusing the ROCm build of PyTorch already installed.

   .. code:: shell

      pip install --no-cache-dir --no-build-isolation "sam2>=0.4.1"

5. Resolve the remaining ``amd-monailabel`` dependencies.

   .. code:: shell

      pip install --no-cache-dir --upgrade-strategy only-if-needed amd-monailabel \
          --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

6. Verify the installation.

   .. code:: shell

      pip show amd-monailabel

.. _source-build:

Building MONAILabel from source
=================================

Build MONAILabel from source if you intend to develop the library.

1. Download the latest version of MONAILabel from the git repository.

   .. code:: shell

      git clone https://github.com/AMD-Ecosystem/MONAILabel.git
      cd MONAILabel

2. Build a wheel and install it. The build number ties the wheel to the build
   date. Set ``BUILD_OHIF=false`` to skip building the bundled OHIF viewer.

   .. code:: shell

      BUILD_OHIF=false python setup.py bdist_wheel --build-number $(date +'%Y%m%d%H%M')
      pip install dist/amd_monailabel-*.whl

3. Verify the installation.

   .. code:: shell

      python -c "import monailabel, torch; print(torch.cuda.is_available())"

Verify the installation
=======================

MONAILabel and PyTorch for ROCm must be installed in the
active virtual environment. The commands check that the process can detect an AMD GPU.

.. code-block:: python

   import torch, monailabel

   print(torch.cuda.is_available())
   print(torch.cuda.get_device_name(0))

   from monailabel.utils.others.generic import gpu_memory_map
   print(gpu_memory_map())

The command prints output of this form.

.. code:: shell

   True
   AMD Instinct MI300X
   {0: free_mb}

``torch.cuda.is_available()`` returns ``True`` on an AMD GPU with ROCm.
``torch.cuda.get_device_name(0)`` returns the Instinct product name, such as
MI300X or MI355X. ``gpu_memory_map()`` returns free VRAM in MB per device.
