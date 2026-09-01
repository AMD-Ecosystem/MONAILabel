.. SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

.. meta::
  :description: What MONAILabel on ROCm is and which AMD GPUs it targets
  :keywords: MONAILabel, MONAILabel on ROCm, PyTorch-ROCm, AMD Instinct, ROCm

.. _what-is-monailabel:

*******************************************
What is MONAILabel on ROCm
*******************************************

`MONAILabel <https://github.com/Project-MONAI/MONAILabel>`_ is an open-source framework licensed under Apache 2.0.
It provides a server for AI-assisted medical image annotation.
It connects 3D Slicer, OHIF, and QuPath clients to MONAI-powered deep learning models.
Radiologists and researchers can build labeled datasets interactively through active-learning workflows.

MONAILabel on ROCm is the AMD ROCm-enabled release of MONAILabel validated on AMD GPUs.
It brings interactive segmentation, auto-segmentation, and model fine-tuning to AMD GPUs through PyTorch-ROCm.
The public Python API is unchanged.
See :doc:`Overview <reference/overview>` for the AMD-specific code changes.