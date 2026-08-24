.. meta::
  :description: How to contribute AMD ROCm-specific changes to MONAILabel, including validation requirements and running the offline unit test suite
  :keywords: MONAILabel, contributing, ROCm, AMD, pull request

.. _monailabel-contributing:

*******************************************
Contributing to MONAILabel on ROCm
*******************************************

MONAILabel on ROCm is maintained as a port of the upstream `Project-MONAI/MONAILabel <https://github.com/Project-MONAI/MONAILabel>`_ project.
AMD contributions follow the upstream Project MONAI contribution workflow.

General process
===================

To contribute a change, complete the following.

1. Fork `Project-MONAI/MONAILabel <https://github.com/Project-MONAI/MONAILabel>`_ and create your branch from ``main``.
2. Follow the `upstream CONTRIBUTING.md <https://github.com/Project-MONAI/MONAILabel/blob/main/CONTRIBUTING.md>`_ for coding standards, pre-commit hooks, and pull request etiquette.
3. For AMD ROCm-specific changes, submit a pull request to `AMD-Ecosystem/MONAILabel <https://github.com/AMD-Ecosystem/MONAILabel>`_.

AMD ROCm requirements
========================

Before raising a pull request for an AMD ROCm-specific change, confirm the following.

- The change is validated on at least one AMD Instinct GPU.
- ``gpu_memory_map()`` returns non-fallback VRAM readings on AMD hardware.
- The ``/gpu`` endpoint correctly dispatches to ``rocm-smi`` on AMD hardware.
- The offline unit test suite passes. It covers transforms, scribbles, client, active learning, DeepEdit, and utility modules.

Running tests
=================

Install the test dependencies, then run the offline unit suite.

.. code:: shell

   # Install test dependencies
   pip install -r requirements.txt
   pip install parameterized pytorch-ignite pytest-timeout nibabel scikit-image

   # Run the offline unit suite
   python -m pytest \
       tests/unit/transform \
       tests/unit/scribbles \
       tests/unit/client \
       tests/unit/activelearning \
       tests/unit/deepedit \
       tests/unit/utils/test_class_utils.py \
       -v --timeout=300

For AMD-Ecosystem contributions more broadly, see the
`AMD-Ecosystem Contribution Guide <https://rocm.docs.amd.com/projects/rocm-ls/en/latest/contribute/contribution.html>`_.
