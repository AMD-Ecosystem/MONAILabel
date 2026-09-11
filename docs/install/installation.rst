.. SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

.. meta::
  :description: Install MONAILabel on ROCm from AMD PyPI, from source, or with Docker, on AMD Instinct GPUs
  :keywords: ROCm-LS, life sciences, MONAILabel installation, MONAILabel on ROCm

.. _installing-monailabel:

************************************
Installing MONAILabel on ROCm
************************************

This topic discusses how to install hipCIM using the following options:

* :ref:`Recommended: AMD PyPI (for users) <install-package>`
* :ref:`Build from source (for developers) <source-build>`

System requirements
=====================

.. list-table::
  :header-rows: 1
  :widths: 22 22 22 34

  * - ROCm version
    - Ubuntu version
    - Python version
    - AMD Instinct™ GPU
  * - 10.0.0
    - 24.04
    - 3.12
    - MI300X, MI325X, MI355X

PyTorch with a compatible ROCm PyTorch build is required.

.. _install-package:

Installing MONAILabel using AMD PyPI
======================================

From within the Docker container where MONAI was installed, use the following commands to install MONAILabel.

1. `Install MONAI <https://rocm.docs.amd.com/projects/monai/en/docs-26.08/install/installation.html>`_.

   MONAI is installed within a Docker container. Run the next commands from within the same Docker container.

2. Set the environment variables.

   .. code:: shell

      export ROCM_HOME=/opt/rocm ROCM_PATH=/opt/rocm HIP_PATH=/opt/rocm \
      AMDGPU_TARGETS=gfx942 HIP_VISIBLE_DEVICES=0

3. Install ``amd-monailabel`` without its dependencies.

   .. code:: shell

      pip install --no-cache-dir --no-deps amd-monailabel \
         --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

4. Install SAM-2, reusing the ROCm bui1ld of PyTorch already installed.

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

From within the Docker container where MONAI was installed, use the following commands to build MONAILabel from source.

1. `Install MONAI <https://rocm.docs.amd.com/projects/monai/en/docs-26.08/install/installation.html>`_.

   MONAI is installed within a Docker container. Run the next commands from within the same Docker container.

2. Set the environment variables.

   .. code:: shell

      export ROCM_HOME=/opt/rocm ROCM_PATH=/opt/rocm HIP_PATH=/opt/rocm \
      AMDGPU_TARGETS=gfx942 HIP_VISIBLE_DEVICES=0

3. Download the latest version of MONAILabel from the git repository.

   .. code:: shell

      git clone https://github.com/AMD-Ecosystem/MONAILabel.git
      cd MONAILabel

4. Build a wheel and install it. The build number ties the wheel to the build
   date. Set ``BUILD_OHIF=false`` to skip building the bundled OHIF viewer.

   .. code:: shell

      BUILD_OHIF=false python setup.py bdist_wheel --build-number $(date +'%Y%m%d%H%M')
      pip install dist/amd_monailabel-*.whl

.. _verify_install:

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

The command prints returns the free VRAM in MB per device:

.. code:: shell

   True
   AMD Instinct MI300X
   {0: free_mb}

``torch.cuda.is_available()`` returns ``True`` on an AMD GPU with ROCm.
``torch.cuda.get_device_name(0)`` returns the Instinct product name, such as
MI300X or MI355X. ``gpu_memory_map()`` returns free VRAM in MB per device.
