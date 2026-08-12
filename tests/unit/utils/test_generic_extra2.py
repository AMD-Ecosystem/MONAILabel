# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import unittest
from unittest import mock

from monailabel.utils.others.generic import (
    create_dataset_from_path,
    get_zoo_bundle,
    is_openslide_supported,
    name_to_device,
    strtobool,
)


class TestStrtobool(unittest.TestCase):
    def test_none(self):
        self.assertFalse(strtobool(None))

    def test_bool_passthrough(self):
        self.assertTrue(strtobool(True))
        self.assertFalse(strtobool(False))

    def test_strings(self):
        self.assertTrue(strtobool("yes"))
        self.assertTrue(strtobool("1"))
        self.assertFalse(strtobool("no"))
        self.assertFalse(strtobool("0"))


class TestIsOpenslideSupported(unittest.TestCase):
    def test_supported(self):
        self.assertTrue(is_openslide_supported("slide.svs"))
        self.assertTrue(is_openslide_supported("a/b/x.tiff"))

    def test_unsupported(self):
        self.assertFalse(is_openslide_supported("image.nii.gz"))
        self.assertFalse(is_openslide_supported("noext"))


class TestNameToDevice(unittest.TestCase):
    def test_explicit_cpu(self):
        self.assertEqual(name_to_device("cpu"), "cpu")

    def test_list_input(self):
        # list -> first element used
        out = name_to_device(["cpu", "cuda"])
        self.assertEqual(out, "cpu")

    def test_cuda_falls_back_to_cpu_when_unavailable(self):
        with mock.patch("monailabel.utils.others.generic.torch.cuda.is_available", return_value=False):
            self.assertEqual(name_to_device("cuda"), "cpu")


class TestCreateDatasetFromPath(unittest.TestCase):
    def test_matched_pairs(self):
        with tempfile.TemporaryDirectory() as d:
            img_dir = os.path.join(d, "images")
            lab_dir = os.path.join(d, "labels")
            os.makedirs(img_dir)
            os.makedirs(lab_dir)
            for name in ("a", "b"):
                open(os.path.join(img_dir, f"{name}.jpg"), "w").close()
                open(os.path.join(lab_dir, f"{name}.png"), "w").close()
            # add a mismatched image with no matching label
            open(os.path.join(img_dir, "c.jpg"), "w").close()
            open(os.path.join(lab_dir, "zzz.png"), "w").close()

            ds = create_dataset_from_path(d)
            names = sorted(os.path.splitext(os.path.basename(x["image"]))[0] for x in ds)
            self.assertEqual(names, ["a", "b"])
            for entry in ds:
                self.assertIn("image", entry)
                self.assertIn("label", entry)


class TestGetZooBundleNoModels(unittest.TestCase):
    def test_no_models_exits(self):
        # With models=None the function prints available bundles and exit(-1).
        with mock.patch(
            "monailabel.utils.others.generic.get_all_bundles_list", return_value=[]
        ), mock.patch("monailabel.utils.others.generic.get_bundle_versions", return_value={"all_versions": []}):
            with self.assertRaises(SystemExit):
                get_zoo_bundle(model_dir="/tmp", conf={}, models=None, conf_key="models")


if __name__ == "__main__":
    unittest.main()
