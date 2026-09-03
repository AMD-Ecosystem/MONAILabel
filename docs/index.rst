.. SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

.. meta::
  :description: MONAILabel is an open-source server for AI-assisted medical image annotation, with an AMD ROCm port for AMD Instinct GPUs.
  :keywords: ROCm-LS, life sciences, MONAILabel, MONAILabel on ROCm document, AMD MONAILabel, ROCm MONAILabel

.. _index:

*******************************************
MONAILabel on ROCm documentation
*******************************************

`MONAILabel <https://github.com/Project-MONAI/MONAILabel>`_ is an open-source framework that provides a server for AI-assisted medical image annotation.
It connects 3D Slicer, OHIF, and QuPath clients to `MONAI <https://project-monai.github.io/>`_-powered deep learning models, providing a means for radiologists and researchers to build labeled datasets interactively through active-learning workflows.

MONAILabel on ROCm is the AMD ROCm-enabled release of MONAILabel validated on AMD GPUs. It brings interactive segmentation, auto-segmentation, and model fine-tuning to AMD GPUs through PyTorch-ROCm.

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

The code is open and hosted at `<https://github.com/AMD-Ecosystem/MONAILabel>`_.

.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Install

    * :ref:`installing-monailabel`
    
  .. grid-item-card:: Related content

    * `MONAILabel blog <https://advanced-micro-devices-rocm-blogs--281.com.readthedocs.build/projects/preview/en/281/>`_

To contribute to MONAILabel on ROCm, see
`Contributing to MONAILabel <https://github.com/AMD-Ecosystem/MONAILabel/blob/amd-integration/CONTRIBUTING.md>`_.

Licensing information is on the :doc:`Licensing <license>` page.
