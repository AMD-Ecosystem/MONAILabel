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

The code is open and hosted at `<https://github.com/AMD-Ecosystem/MONAILabel>`_.

.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Install

    * :ref:`installing-monailabel`

  .. grid-item-card:: Reference

    * :doc:`Overview <reference/overview>`

  .. grid-item-card:: Related content

    * `MONAILabel blog <https://advanced-micro-devices-rocm-blogs--281.com.readthedocs.build/projects/preview/en/281/>`_

To contribute to MONAILabel on ROCm, see
`Contributing to MONAILabel <https://github.com/AMD-Ecosystem/MONAILabel/blob/amd-integration/CONTRIBUTING.md>`_.

Licensing information is on the :doc:`Licensing <license>` page.
