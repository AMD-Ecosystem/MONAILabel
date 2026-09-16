<!--
Copyright (c) MONAI Consortium
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Modifications Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.
-->

# AMD-MONAILabel (AMD ROCm)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

> **Runs on AMD Instinct GPUs** — the AMD ROCm port is validated on AMD Instinct MI300X, MI325X, and MI355X,
> and is compatible with `amd-monai` 1.6.0, Python 3.12, and PyTorch for ROCm 10.0.0.
> See [Step 1 Installation (ROCm)](#step-1-installation) for the install path, or jump to the
> [Verify the installation](#quick-verify) snippet.

MONAILabel is an intelligent open source image labeling and learning tool that enables users to create annotated datasets and build AI annotation models for clinical evaluation. MONAILabel enables application developers to build labeling apps in a serverless way, where custom labeling apps are exposed as a service through the MONAILabel Server.

MONAILabel is a server-client system that facilitates interactive medical image annotation by using AI. It is an
open-source and easy-to-install ecosystem that can run locally on a machine with single or multiple GPUs. Both server
and client work on the same/different machine. It shares the same principles
with [MONAI](https://github.com/Project-MONAI).


### Table of Contents
- [Overview](#overview)
  - [Highlights and Features](#highlights-and-features)
  - [Supported Matrix](#supported-matrix)
- [Getting Started with MONAILabel](#getting-started-with-monai-label)
  - [Step 1. Installation](#step-1-installation)
  - [Step 2. MONAILabel Sample Applications](#step-2-monai-label-sample-applications)
  - [Step 3. Data Preparation](#step-3-data-preparation)
  - [Step 4. Start MONAILabel Server and Start Annotating!](#step-4-start-monai-label-server-and-start-annotating)
- [OHIF Web Viewer (AMD ROCm)](#ohif-web-viewer-amd-rocm)
- [MONAILabel Tutorials](#monai-label-tutorials)
- [Cite MONAILabel](#cite)
- [Contributing](#contributing)
- [Community](#community)
- [Additional Resources](#additional-resources)

### Overview
MONAILabel reduces the time and effort of annotating new datasets and enables the adaptation of AI to the task at hand by continuously learning from user interactions and data. MONAILabel allows researchers and developers to make continuous improvements to their apps by allowing them to interact with their apps at the user would. End-users (clinicians, technologists, and annotators in general) benefit from AI continuously learning and becoming better at understanding what the end-user is trying to annotate.

MONAILabel aims to fill the gap between developers creating new annotation applications, and the end users which want to benefit from these innovations.

#### Highlights and Features
- Framework for developing and deploying MONAILabel Apps to train and infer AI models
- Compositional & portable APIs for ease of integration in existing workflows
- Customizable labeling app design for varying user expertise
  & [OHIF](https://github.com/AMD-Ecosystem/MONAILabel/tree/main/plugins/ohif) for radiology
- PACS connectivity via [DICOMWeb](https://www.dicomstandard.org/using/dicomweb)
- Automated Active Learning workflow for endoscopy using [CVAT](https://github.com/AMD-Ecosystem/MONAILabel/tree/main/plugins/cvat)

#### Supported Matrix

MONAILabel supports many state-of-the-art(SOTA) models in Model-Zoo, and their integration with viewers and monaibundle app. Please refer to [monaibundle](https://github.com/AMD-Ecosystem/MONAILabel/tree/main/sample-apps/monaibundle) app page for supported models, including whole body segmentation, whole brain segmentation, lung nodule detection, tumor segmentation and many more.

In addition, you can find a table of the basic supported fields, modalities, viewers, and general data types.  However, these are only ones that we've explicitly test and that doesn't mean that your dataset or file type won't work with MONAILabel.  Try MONAI for your given task and if you're having issues, reach out through GitHub Issues.
<table>
<tr>
  <th>Field</th>
  <th>Models</th>
  <th>Viewers</th>
  <th>Data Types</th>
  <th>Image Modalities/Target</th>
</tr>
  <td>Radiology</td>
  <td>
    <ul>
      <li>Segmentation</li>
      <li>DeepGrow</li>
      <li>DeepEdit</li>
      <li>SAM2 (2D/3D)</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>3DSlicer</li>
      <li>MITK</li>
      <li>OHIF</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>NIfTI</li>
      <li>NRRD</li>
      <li>DICOM</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>CT</li>
      <li>MRI</li>
    </ul>
  </td>
<tr>
</tr>
  <td>Pathology</td>
  <td>
    <ul>
      <li>DeepEdit</li>
      <li>NuClick</li>
      <li>Segmentation</li>
      <li>Classification</li>
      <li>SAM2 (2D)</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>Digital Slide Archive</li>
      <li>QuPath</li>
      <li>CVAT</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>TIFF</li>
      <li>SVS</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>Nuclei Segmentation</li>
      <li>Nuclei Classification</li>
    </ul>
  </td>
<tr>
</tr>
  <td>Video</td>
  <td>
    <ul>
      <li>DeepEdit</li>
      <li>Tooltracking</li>
      <li>InBody/OutBody</li>
      <li>SAM2 (2D)</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>CVAT</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>JPG</li>
      <li>3-channel Video Frames</li>
    </ul>
  </td>
  <td>
    <ul>
      <li>Endoscopy</li>
    </ul>
  </td>
<tr>
</table>

# Getting Started with MONAILabel
### MONAILabel requires a few steps to get started:
- Step 1: [Install MONAILabel](#step-1-installation) 
- Step 2: [Download a MONAILabel sample app or write your own custom app](#step-2-monai-label-sample-applications)
- Step 3: [Prepare your Data](#step-3-data-preparation)
- Step 4: [Launch MONAILabel Server and start Annotating!](#step-4-start-monai-label-server-and-start-annotating)

## Step 1 Installation

### ROCm (AMD GPU) Build

**System requirements**

| ROCm version | Ubuntu version | Python version | AMD Instinct™ GPU |
| --- | --- | --- | --- |
| 10.0.0 | 24.04 | 3.12 | MI300X, MI325X, MI355X |

PyTorch with a compatible ROCm PyTorch build is required.

MONAI is installed within a Docker container. Run the commands below from within that same container after
[installing MONAI](https://rocm.docs.amd.com/projects/monai/en/docs-26.08/install/installation.html).

In both paths, first set the environment variables:

```bash
# Set AMDGPU_TARGETS to your GPU architecture: gfx942 for MI300X/MI325X, gfx950 for MI355X.
export ROCM_HOME=/opt/rocm ROCM_PATH=/opt/rocm HIP_PATH=/opt/rocm \
AMDGPU_TARGETS=gfx942 HIP_VISIBLE_DEVICES=0
```

**Recommended: install from AMD PyPI (for users)**

```bash
# 1. Install amd-monailabel without its dependencies
pip install --no-cache-dir --no-deps amd-monailabel \
   --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

# 2. Install SAM-2, reusing the ROCm build of PyTorch already installed
pip install --no-cache-dir --no-build-isolation "sam2>=0.4.1"

# 3. Resolve the remaining amd-monailabel dependencies
pip install --no-cache-dir --upgrade-strategy only-if-needed amd-monailabel \
   --extra-index-url=https://pypi.amd.com/rocm-10.0.0/simple/

# 4. Verify the installation
pip show amd-monailabel
```

**Build from source (for developers)**

```bash
git clone https://github.com/AMD-Ecosystem/MONAILabel.git
cd MONAILabel

# The build number ties the wheel to the build date.
# Set BUILD_OHIF=false to skip building the bundled OHIF viewer.
BUILD_OHIF=false python setup.py bdist_wheel --build-number $(date +'%Y%m%d%H%M')
pip install dist/amd_monailabel-*.whl
```

**Verify the installation** <a name="quick-verify"></a>

MONAILabel and PyTorch for ROCm must be installed in the active virtual environment. These commands check that
the process can detect an AMD GPU:

```python
import torch, monailabel
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

from monailabel.utils.others.generic import gpu_memory_map
print(gpu_memory_map())
```

Expected output:

```
True
AMD Instinct MI300X
{0: free_mb}
```

`torch.cuda.is_available()` returns `True` on an AMD GPU with ROCm. `torch.cuda.get_device_name(0)` returns the
Instinct product name, such as MI300X or MI355X. `gpu_memory_map()` returns free VRAM in MB per device.

### GPU Acceleration (Optional Dependencies)
The following optional dependencies can accelerate GPU-based transforms from MONAI on AMD hardware:
- [HIPCIM](https://github.com/AMD-Ecosystem/hipCIM) — ROCm-compatible replacement for cucim
- [ROCm Toolkit](https://rocm.docs.amd.com/en/latest/)

### SAM-2

> By default, [**SAM2**](https://github.com/facebookresearch/sam2/) model is included for all the Apps when **_python >= 3.12_**
>  - **sam_2d**: for any organ or tissue and others over a given slice/2D image.
>  - **sam_3d**: to support SAM2 propagation over multiple slices (Radiology/MONAI-Bundle).

To use [SAM-2.1](https://huggingface.co/facebook/sam2.1-hiera-large), run in dev mode (git checkout) or install the latest **SAM-2** from its [github](https://github.com/facebookresearch/sam2/tree/main?tab=readme-ov-file#installation).

## Step 2 MONAILabel Sample Applications

<h3>Radiology</h3>
<p>This app has example models to do both interactive and automated segmentation over radiology (3D) images. Including auto segmentation with the latest deep learning models (e.g., UNet, UNETR) for multiple abdominal organs. Interactive tools include DeepEdit and Deepgrow for actively improving trained models and deployment.</p>
<ul>
  <li>Deepedit</li>
  <li>Deepgrow</li>
  <li>Segmentation</li>
  <li>Spleen Segmentation</li>
  <li>Multi-Stage Vertebra Segmentation</li>
</ul>

<h3>Pathology</h3>
<p>This app has example models to do both interactive and automated segmentation over pathology (WSI) images. Including nuclei multi-label segmentation for Neoplastic cells, Inflammatory, Connective/Soft tissue cells, Dead Cells, and Epithelial. The app provides interactive tools including DeepEdits for interactive nuclei segmentation.</p>
<ul>
  <li>NuClick</li>
  <li>Nuclei Segmentation</li>
  <li>Nuclei Classification</li>
  <li>HoVerNet</li>
  <li>SAM2 (2D)</li>
</ul>
<h3>Video</h3>
<p>The Endoscopy app enables users to use interactive, automated segmentation and classification models over 2D images for endoscopy usecase. Combined with CVAT, it will demonstrate the fully automated Active Learning workflow to train + fine-tune a model.</p>
<ul>
  <li>Deepedit</li>
  <li>ToolTracking</li>
  <li>InBody/OutBody</li>
</ul>
<h3>Bundles</h3>
<p>The Bundle app enables users with customized models for inference, training or pre and post processing any target anatomies. The specification for MONAILabel integration of the Bundle app links archived Model-Zoo for customized labeling (e.g., the third-party transformer model for labeling renal cortex, medulla, and pelvicalyceal system. Interactive tools such as DeepEdits).</p>

For a full list of supported bundles, see the <a href="https://github.com/AMD-Ecosystem/MONAILabel/tree/main/sample-apps/monaibundle">MONAILabel Bundles README</a>.

## Step 3 Data Preparation
For data preparation, you have two options, you can use a local data store or any image archive tool that supports DICOMWeb.

#### Local Datastore for the Radiology App on single modality images
For a Datastore in a local file archive, there is a set folder structure that MONAILabel uses. Place your image data in a folder and if you have any segmentation files, create and place them in a subfolder called `labels/final`. You can see an example below:
```
dataset
│-- spleen_10.nii.gz
│-- spleen_11.nii.gz
│   ...
└───labels
    └─── final
        │-- spleen_10.nii.gz
        │-- spleen_11.nii.gz
        │   ...
```

If you don't have labels, just place the images/volumes in the dataset folder.

#### DICOMWeb Support
If the viewer you're using supports DICOMweb standard, you can use that instead of a local datastore to serve images to MONAILabel. When starting the MONAILabel server, we need to specify the URL of the DICOMweb service in the studies argument (and, optionally, the username and password for DICOM servers that require them). You can see an example of starting the MONAILabel server with a DICOMweb URL below:


```
monailabel start_server --app apps/radiology --studies http://127.0.0.1:8042/dicom-web --conf models segmentation
```

## Step 4 Start MONAILabel Server and Start Annotating
You're now ready to start using MONAILabel.  Once you've configured your viewer, app, and datastore, you can launch the MONAILabel server with the relevant parameters. For simplicity, you can see an example where we download a Radiology sample app and dataset, then start the MONAILabel server below:

```
monailabel apps --download --name radiology --output apps
monailabel datasets --download --name Task09_Spleen --output datasets
monailabel start_server --app apps/radiology --studies datasets/Task09_Spleen/imagesTr --conf models segmentation
```
## OHIF Web Viewer (AMD ROCm)

The OHIF Viewer is built into the AMD ROCm Docker image (`BUILD_OHIF=true`) and is
served directly by the MONAILabel server at the `/ohif/` path. OHIF reads studies
from a DICOMweb data source, so the flow is: run an Orthanc DICOMweb server, load
DICOM studies into it, then start the MONAILabel server pointed at Orthanc.

The steps below were validated end-to-end on an AMD MI300X node using the
`amd-monailabel:latest` image built from the [Dockerfile](Dockerfile).

### 1. Start Orthanc (DICOMweb data source)

```bash
cat > orthanc.json <<'JSON'
{
  "Name": "orthanc-ml",
  "Plugins": [ "/usr/local/share/orthanc/plugins/" ],
  "DicomWeb": { "Enable": true, "Root": "/dicom-web/" },
  "RemoteAccessAllowed": true,
  "AuthenticationEnabled": false
}
JSON

docker run -d --name orthanc-ml --network host \
  -v "$PWD/orthanc.json:/etc/orthanc/orthanc.json:ro" \
  jodogne/orthanc-plugins

# DICOMweb should now answer on http://127.0.0.1:8042/dicom-web/studies
```

> The `Plugins` path is required — mounting your own `orthanc.json` overrides the
> image default, so the DICOMweb plugin will not load unless you point at the
> plugins directory explicitly.

### 2. Load DICOM studies into Orthanc

If your data is NIfTI (e.g. `Task09_Spleen`), convert a few volumes to DICOM
series first (any converter using `pydicom.generate_uid()` for valid UIDs — plain
`1.2.826...` string UIDs are rejected by pydicom at inference time), then upload:

```bash
# upload every .dcm under ./spleen_dicom to Orthanc
find ./spleen_dicom -name '*.dcm' -exec \
  curl -s -o /dev/null -X POST http://127.0.0.1:8042/instances \
       --data-binary @{} -H "Content-Type: application/dicom" \;

# verify studies are visible over DICOMweb
curl -s http://127.0.0.1:8042/dicom-web/studies | head
```

### 3. Start the MONAILabel server (serves OHIF)

Run the server from the ROCm image with the GPU attached and `--studies` pointing
at Orthanc's DICOMweb endpoint:

```bash
docker run -d --name ml_server --network host \
  --device=/dev/kfd --device=/dev/dri --group-add video \
  --ipc=host --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --shm-size=8G \
  amd-monailabel:latest bash -lc '
    cp -r /usr/local/monailabel/sample-apps/radiology /workspace/radiology
    HIP_VISIBLE_DEVICES=0 PYTORCH_HIP_ALLOC_CONF=expandable_segments:True \
    MLFLOW_ALLOW_FILE_STORE=true \
    monailabel start_server \
      --app /workspace/radiology \
      --studies http://127.0.0.1:8042/dicom-web \
      --conf models all \
      --host 0.0.0.0 --port 8000'
```

`--conf models all` exposes every radiology model (segmentation, deepedit,
deepgrow_2d/3d, sw_fastedit, sam_2d/3d, spine localization/segmentation
pipelines, and the GraphCut scribbles post-processors). Use
`--conf models segmentation` for a lighter startup.

### 4. Open the viewer

```bash
# from your laptop, tunnel to the node:
ssh -L 8000:127.0.0.1:8000 -J <login-host> <user>@<gpu-node>
```

Then browse to **http://localhost:8000/ohif/** (not `/`, which serves the Swagger
API docs). Use an **incognito window** — OHIF's service worker caches the old
bundle, so a normal refresh is often not enough. The AI models appear in the
right-hand **MONAILabel** panel.

### Known limitation (this release)

Manual **annotation is not available** in this build: the manual-markup toolbar
(Brush / Eraser / ROI / Length / Arrow) is disabled, and triggering annotation
can blank the viewer. This is a front-end OHIF-plugin version-drift issue (the
`monai-label` extension targets a newer OHIF than the pinned build); the MONAI
Label server itself is unaffected. Auto-segmentation and the model actions in the
MONAILabel side panel work as expected.

## Cite

If you are using MONAILabel in your research, please use the following citation:

```bash
@article{DiazPinto2022monailabel,
   author = {Diaz-Pinto, Andres and Alle, Sachidanand and Ihsani, Alvin and Asad, Muhammad and
            Nath, Vishwesh and P{\'e}rez-Garc{\'\i}a, Fernando and Mehta, Pritesh and
            Li, Wenqi and Roth, Holger R. and Vercauteren, Tom and Xu, Daguang and
            Dogra, Prerna and Ourselin, Sebastien and Feng, Andrew and Cardoso, M. Jorge},
    title = {{MONAILabel: A framework for AI-assisted Interactive Labeling of 3D Medical Images}},
  journal = {arXiv e-prints},
     year = 2022,
     url  = {https://arxiv.org/pdf/2203.12362.pdf}
}

@inproceedings{DiazPinto2022DeepEdit,
      title={{DeepEdit: Deep Editable Learning for Interactive Segmentation of 3D Medical Images}},
      author={Diaz-Pinto, Andres and Mehta, Pritesh and Alle, Sachidanand and Asad, Muhammad and Brown, Richard and Nath, Vishwesh and Ihsani, Alvin and Antonelli, Michela and Palkovics, Daniel and Pinter, Csaba and others},
      booktitle={MICCAI Workshop on Data Augmentation, Labelling, and Imperfections},
      pages={11--21},
      year={2022},
      organization={Springer}
}
 ```

Optional Citation: if you are using active learning functionality from MONAILabel, please support us:

```bash
@article{nath2020diminishing,
  title={Diminishing uncertainty within the training pool: Active learning for medical image segmentation},
  author={Nath, Vishwesh and Yang, Dong and Landman, Bennett A and Xu, Daguang and Roth, Holger R},
  journal={IEEE Transactions on Medical Imaging},
  volume={40},
  number={10},
  pages={2534--2547},
  year={2020},
  publisher={IEEE}
}
```

## Contributing

For guidance on making a contribution to MONAILabel, see
the [contributing guidelines](https://github.com/AMD-Ecosystem/MONAILabel/blob/main/CONTRIBUTING.md).


Ask and answer questions over
on [MONAILabel's GitHub Discussions tab](https://github.com/AMD-Ecosystem/MONAILabel/discussions).

## Additional Resources

- Upstream project: https://github.com/Project-MONAI/MONAILabel
- AMD ROCm fork: https://github.com/AMD-Ecosystem/MONAILabel
- API documentation: https://monai.readthedocs.io/projects/label
- Issue tracker: https://github.com/AMD-Ecosystem/MONAILabel/issues
