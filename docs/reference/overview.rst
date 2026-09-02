.. SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

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

ROCm ships a PyTorch build where HIP presents itself as CUDA through the ``torch.cuda`` namespace.
MONAILabel uses ``torch.cuda.is_available()``, ``tensor.cuda()``, and ``model.to("cuda")``.
Those calls work on AMD hardware without application changes.
AMD systems query VRAM with ``rocm-smi`` instead of ``nvidia-smi``.

The port is validated on AMD Instinct MI300X, MI325X, and MI355X.
It is compatible with ``amd-monai`` 1.6.0, Python 3.12, and PyTorch for ROCm 10.0.0.

The AMD ROCm port makes these changes to upstream MONAILabel.

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
    - Documents an AMD ROCm 10.0.0 base image and the AMD PyPI wheel index as an alternative to the default CUDA-based installation.
