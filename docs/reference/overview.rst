.. meta::
  :description: What MONAILabel on ROCm is and what the AMD port changed
  :keywords: MONAILabel, MONAILabel on ROCm, PyTorch-ROCm, rocm-smi, AMD

.. _monailabel-overview:

*******************************************
MONAILabel on ROCm overview
*******************************************

MONAILabel is an open-source framework licensed under Apache 2.0.
It provides a server for AI-assisted medical image annotation.
It connects 3D Slicer, OHIF, and QuPath clients to MONAI-powered deep learning models.
Radiologists and researchers can build labeled datasets interactively through active-learning workflows.

The AMD ROCm port runs MONAILabel on AMD GPUs without requiring changes to application code.
All GPU compute runs through PyTorch-ROCm.
``torch.cuda.*`` APIs map to HIP on AMD hardware.
There are no new GPU kernels and no change to the public Python API.

The AMD ROCm port makes the following changes to upstream MONAILabel:

.. list-table::
  :header-rows: 1
  :widths: 30 70

  * - File
    - Change
  * - ``monailabel/utils/others/generic.py``
    - ``gpu_memory_map()`` adds a ``rocm-smi`` fallback for AMD GPU VRAM queries when ``nvidia-smi`` is absent. The function returns free VRAM in MB per device. MONAILabel automatic image-size tuning uses that value.
  * - ``monailabel/endpoints/logs.py``
    - The ``/gpu`` admin endpoint dispatches to ``nvidia-smi`` on NVIDIA systems or ``rocm-smi`` on AMD systems, whichever is present.
  * - ``Dockerfile``
    - Documents an AMD ROCm 10.0 base image and the AMD PyPI wheel index as an alternative to the default CUDA-based installation.

Validated GPUs and software versions are on the :doc:`Compatibility matrix <compatibility-matrix>`.
