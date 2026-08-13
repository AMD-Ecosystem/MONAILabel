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

from monailabel.utils.others.generic import get_bundle_models, get_zoo_bundle


class TestGetBundleModelsLocalSource(unittest.TestCase):
    def test_local_existing_bundle_dir(self):
        # zoo_source != monaihosting -> local branch; existing dir avoids download
        with tempfile.TemporaryDirectory() as app_dir:
            model_dir = os.path.join(app_dir, "model")
            os.makedirs(os.path.join(model_dir, "mybundle"))
            conf = {"zoo_source": "local", "models": "mybundle"}
            bundles = get_bundle_models(app_dir, conf, conf_key="models")
            self.assertIn("mybundle", bundles)
            self.assertTrue(bundles["mybundle"].endswith(os.path.join("model", "mybundle")))

    def test_local_ngc_download_versioned(self):
        # non-existing dir with _v<version> -> NGC branch, download mocked
        with tempfile.TemporaryDirectory() as app_dir:
            conf = {"zoo_source": "ngc", "models": "spleen_ct_segmentation_v0.4.0"}
            with mock.patch("monailabel.utils.others.generic.download") as dl:
                bundles = get_bundle_models(app_dir, conf, conf_key="models")
                self.assertIn("spleen_ct_segmentation_v0.4.0", bundles)
                dl.assert_called_once()


class TestGetZooBundleInvalidModels(unittest.TestCase):
    def test_invalid_models_exit(self):
        # models not in zoo and not local dirs -> prints + exit(-1)
        with tempfile.TemporaryDirectory() as model_dir:
            with mock.patch(
                "monailabel.utils.others.generic.get_all_bundles_list",
                return_value=[("some_bundle", "x")],
            ), mock.patch(
                "monailabel.utils.others.generic.get_bundle_versions",
                return_value={"all_versions": ["0.1.0"]},
            ):
                with self.assertRaises(SystemExit):
                    get_zoo_bundle(model_dir, conf={}, models=["totally_invalid_model"], conf_key="models")


if __name__ == "__main__":
    unittest.main()
