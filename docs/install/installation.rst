.. meta::
  :description: Install MONAILabel on ROCm from AMD PyPI, from source, or with Docker, on AMD Instinct GPUs
  :keywords: ROCm-LS, life sciences, MONAILabel installation, MONAILabel on ROCm

.. _installing-monailabel:

************************************
Installing MONAILabel on ROCm
************************************

MONAILabel on ROCm can be installed using :ref:`AMD PyPI and upstream PyPI <install-package>` or it can be :ref:`built from source <source-build>`.

System requirements
===================

+--------------+----------------+----------------+----------------------------------+
| ROCm version | Ubuntu version | Python version | AMD Instinct GPU (tested)        |
+==============+================+================+==================================+
| 10.0         | 24.04          | 3.12           | MI300X, MI325X, MI350X, MI355X   |
+--------------+----------------+----------------+----------------------------------+

.. note::

   Ubuntu 24.04 is the tested reference operating system.
   The install requires ``amd-monai`` 1.6.0 and PyTorch ``2.13.0+rocm7.1`` or a compatible ROCm build.
   For other validated combinations, see :doc:`Compatibility matrix <../reference/compatibility-matrix>`.

Setting up the environment
----------------------------

Set up the environment for installing MONAILabel on ROCm.

1. Optionally start an Ubuntu 24.04 Docker container with the ROCm base image.

   .. code:: shell

      docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true \
          --shm-size=128GB --network=host --device=/dev/kfd \
          --device=/dev/dri --group-add video -it \
          -v $HOME:$HOME --name ${LOGNAME}_rocm \
          rocm/dev-ubuntu-24.04:7.15-complete

2. Create and activate a Python virtual environment.

   .. code:: shell

      python3 -m venv monailabel_env
      source monailabel_env/bin/activate
      pip install --upgrade pip

3. Set the environment variables. Set ``AMDGPU_TARGETS`` to the GFX target for
   your GPU. Use only one value.

   .. code:: shell

      export ROCM_HOME=/opt/rocm
      export ROCM_PATH=/opt/rocm
      export HIP_PATH=/opt/rocm
      export HIP_VISIBLE_DEVICES=0
      # MI300X / MI325X
      export AMDGPU_TARGETS=gfx942
      # MI350X / MI355X
      # export AMDGPU_TARGETS=gfx950

.. _source-build:

Building MONAILabel from source
=================================

Build MONAILabel from source if you intend to develop for the library.

1. Download the latest version of MONAILabel from the git repository.

   .. code:: shell

      git clone https://github.com/AMD-Ecosystem/MONAILabel.git
      cd MONAILabel

2. Build a wheel and install it. The build number ties the wheel to the build
   date. Set ``BUILD_OHIF=false`` to skip building the bundled OHIF viewer.

   .. code:: shell

      BUILD_OHIF=false python setup.py bdist_wheel --build-number $(date +'%Y%m%d%H%M')
      pip install dist/monailabel-*.whl

3. Verify the installation.

   .. code:: shell

      python -c "import monailabel, torch; print(torch.cuda.is_available())"

.. _install-package:

Installing MONAILabel using AMD PyPI
======================================

If you don't intend to develop for the library, install the ROCm-validated
``amd-monai`` dependency from `AMD PyPI <https://pypi.amd.com/simple/>`_, then
install ``monailabel`` from upstream PyPI. pip uses the already-installed
``amd-monai`` package instead of pulling the standard ``monai`` package.

Finish the environment setup before you install from PyPI.

1. Install the ROCm-validated MONAI build from AMD PyPI.

   .. code:: shell

      pip install "amd-monai==1.6.0" \
          --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

2. Install PyTorch for ROCm before any other package.
   Finish this install before the remaining packages.
   Later resolution might otherwise pull in a CUDA build.

   .. code:: shell

      pip install --no-cache-dir torch torchvision torchaudio \
          --index-url https://download.pytorch.org/whl/rocm7.1

3. Install ``monailabel`` without its dependencies.
   ``--no-deps`` stops pip from replacing the ROCm build of PyTorch with a CUDA-linked build.
   That replacement can happen while pip resolves the transitive requirements of ``monailabel``.

   .. code:: shell

      pip install --no-cache-dir --no-deps monailabel

4. Install SAM-2, reusing the ROCm build of PyTorch already installed.
   ``--no-build-isolation`` stops pip from creating an isolated build environment.
   An isolated environment might independently pull and compile against a CUDA build of PyTorch.

   .. code:: shell

      pip install --no-cache-dir --no-build-isolation "sam2>=0.4.1"

5. Resolve the remaining ``monailabel`` dependencies.
   ``--upgrade-strategy only-if-needed`` satisfies missing dependencies without upgrading the ROCm build of PyTorch installed in step 2.

   .. code:: shell

      pip install --no-cache-dir --upgrade-strategy only-if-needed monailabel

6. Verify the installation.

   .. code:: shell

      pip show -v monailabel

Getting started
=================

The following sample assumes MONAILabel and PyTorch for ROCm are installed in the
active virtual environment. It checks that the process can detect an AMD GPU.

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
