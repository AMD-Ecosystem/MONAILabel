.. SPDX-FileCopyrightText: Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
.. SPDX-License-Identifier: Apache-2.0

.. meta::
  :description: New features, correctness fixes, and known limitations in the first AMD ROCm-enabled release of MONAILabel
  :keywords: MONAILabel, release notes, ROCm, AMD, MONAI Label

.. _monailabel-whats-new:

**************************************************
Release notes for MONAILabel 0.8.5 on ROCm
**************************************************

MONAILabel 0.8.5 on ROCm is the first AMD ROCm-enabled release of MONAILabel.
It targets ROCm 10.0, Python 3.12, and MONAI 1.6.0.

Supported components
====================

This release supports these components.

.. list-table::
  :header-rows: 1
  :widths: 40 60

  * - Component
    - Supported
  * - AMD Instinct GPU
    - MI300X, MI325X, and MI355X
  * - ROCm
    - 10.0
  * - Ubuntu
    - 24.04
  * - Python
    - 3.12
  * - PyTorch
    - 2.13.0+rocm7.1

Features
========

MONAILabel 0.8.5 on ROCm includes these features.

ROCm enablement
---------------

GPU telemetry and packaging on AMD systems use ROCm tools and images.

- On AMD systems, ``gpu_memory_map()`` and GPU logging both use ``rocm-smi``. The NVIDIA ``nvidia-smi`` fallback is retained.
- The release ships a ROCm-oriented Dockerfile based on ``rocm/dev-ubuntu-24.04:7.15-complete``. Source builds install the ``amd_monailabel-*.whl`` wheel.

Packaging
---------

These packaging changes keep a ROCm environment from pulling CUDA wheels.

- ``amd-constraints.txt`` is in the source repository only. It isn't shipped in the wheel. It pins ``nvidia-*`` and ``cuda*`` wheels to ``==0``.
- Install ROCm PyTorch first from the PyTorch ROCm index, then ``amd-monai``, then ``amd-monailabel``.
- Install SAM-2 with ``--no-build-isolation`` so its isolated build doesn't pull CUDA PyTorch.

Correctness fixes
-----------------

These fixes apply upstream as well as on ROCm.

- ``datastore/utils/convert.py`` now creates temp files with ``delete=False`` so that callers no longer lose files when they are garbage-collected.
- The data-dict key ``image_path`` is renamed to ``img_path`` across the infer, writer, cache, and SAM-2 paths. ``Spacingd`` in MONAI treats any ``image_*`` sibling key as a meta dict. The rename avoids that collision.

OHIF web viewer
---------------

The bundled OHIF viewer is updated for this release.

- When ``BUILD_OHIF`` is set, the OHIF v3 viewer builds into the image, and the MONAILabel server serves it at ``/ohif/``. The viewer supports the Orthanc DICOMweb data source.
- The plugin is updated for the pinned OHIF build, fixing icon, dialog, and toolbar API drift.

Supported models
================

The Radiology app supports segmentation, including spleen and vertebra.
It also supports DeepEdit, DeepGrow 2D and 3D, SW-FastEdit, and SAM-2 2D and 3D.
Spine localization and segmentation pipelines are included.
Scribbles-based GraphCut post-processing is included.

Known limitations
=================

These limitations apply to this release.

.. list-table::
  :header-rows: 1
  :widths: 40 60

  * - Limitation
    - Detail
  * - OHIF manual annotation isn't available this release.
    - The manual markup toolbar is disabled, including brush, eraser, and ROI. Triggering annotation can blank the viewer. This is a front-end plugin and OHIF version-drift issue. The MONAILabel server is unaffected. Auto-segmentation and the side-panel model actions work.
  * - CI and build environments must have ``git`` installed.
    - Without it, the SAM-2 git dependency silently fails to install. That drops ``sam2/infer.py`` coverage to zero and disables SAM models.
  * - Lung-nodule detection training is unvalidated on the AMD port.
    - See ``test_007_lung_nodule_detection_train``.
