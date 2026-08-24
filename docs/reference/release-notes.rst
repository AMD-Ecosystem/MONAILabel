.. meta::
  :description: New features, correctness fixes, testing results, and known limitations in the first AMD ROCm-enabled release of MONAILabel
  :keywords: MONAILabel, release notes, ROCm, AMD, MONAI Label

.. _monailabel-whats-new:

*******************************************
What's new in MONAILabel 0.8.5 on ROCm
*******************************************

MONAILabel 0.8.5 on ROCm is the first AMD ROCm-enabled release of MONAILabel.

Supported components
======================

This release supports the following components.

.. list-table::
  :header-rows: 1
  :widths: 40 60

  * - Component
    - Supported
  * - AMD Instinct™ GPU
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
================

MONAILabel 0.8.5 on ROCm includes the following features.

ROCm enablement
------------------

GPU telemetry and packaging on AMD systems use ROCm tools and images.

- On AMD systems, ``gpu_memory_map()`` and GPU logging both use ``rocm-smi``. The NVIDIA ``nvidia-smi`` fallback is retained.
- The release ships a ROCm-oriented Dockerfile based on ``rocm/dev-ubuntu-24.04:7.15-complete`` and a ``monailabel-0.8.5-py3-none-any.whl`` wheel.

Correctness fixes
--------------------

These fixes apply upstream as well as on ROCm.

- ``datastore/utils/convert.py`` now creates temp files with ``delete=False`` so that callers no longer lose files when they are garbage-collected.
- The data-dict key ``image_path`` is renamed to ``img_path`` across the infer, writer, cache, and SAM-2 paths. ``Spacingd`` in MONAI treats any ``image_*`` sibling key as a meta dict. The rename avoids that collision.

OHIF web viewer
-------------------

The bundled OHIF viewer is updated for this release.

- When ``BUILD_OHIF`` is set, the OHIF v3 viewer builds into the image, and the MONAILabel server serves it at ``/ohif/``. The viewer supports the Orthanc DICOMweb data source.
- The plugin is updated for the pinned OHIF build, fixing icon, dialog, and toolbar API drift.

Supported models
====================

The Radiology app supports segmentation, including spleen and vertebra.
It also supports DeepEdit, DeepGrow 2D and 3D, SW-FastEdit, and SAM-2 2D and 3D.
Spine localization and segmentation pipelines are included.
Scribbles-based GraphCut post-processing is included.

Known limitations
=====================

The following limitations apply to this release.

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
