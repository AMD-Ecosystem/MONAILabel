.. meta::
  :description: Validated MONAI, PyTorch, ROCm, Ubuntu, Python, and GPU combinations for MONAILabel on ROCm
  :keywords: MONAILabel, compatibility matrix, ROCm, MONAI, PyTorch, AMD Instinct

.. _monailabel-compatibility:

*******************************************
MONAILabel on ROCm compatibility matrix
*******************************************

The following software combinations have been validated for MONAILabel on ROCm.

.. list-table::
  :header-rows: 1
  :widths: 14 12 20 12 14 12 30

  * - MONAILabel
    - MONAI
    - PyTorch
    - ROCm
    - Ubuntu
    - Python
    - GPU
  * - 0.8.5
    - 1.6.0
    - 2.13.0+rocm7.1
    - 10.0
    - 24.04
    - 3.12
    - MI300X, ``gfx942``, MI325X, ``gfx942``, MI355X, ``gfx950``
  * - 0.8.5
    - 1.5.2
    - 2.10.0+rocm7.2
    - 7.2.0
    - 22.04, 24.04
    - 3.12
    - MI300X, ``gfx942``, MI325X, ``gfx942``, MI355X, ``gfx950``
  * - 0.8.5
    - 1.5.2
    - 2.10.0+rocm7.2
    - 7.2.0
    - 24.04
    - 3.12
    - MI350X, ``gfx950``
  * - 0.8.5
    - 1.5.2
    - 2.9.1+rocm6.4
    - 7.0.2
    - 22.04
    - 3.12
    - MI300X, ``gfx942``

The following AMD Instinct GPUs have been validated.

.. list-table::
  :header-rows: 1
  :widths: 34 22 22

  * - GPU
    - Architecture
    - VRAM
  * - AMD Instinct™ MI300X
    - ``gfx942``
    - 196 GB
  * - AMD Instinct™ MI325X
    - ``gfx942``
    - 256 GB
  * - AMD Instinct™ MI355X
    - ``gfx950``
    - 294 GB
