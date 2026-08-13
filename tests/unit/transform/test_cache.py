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

import unittest

import torch
from monai.data import MetaTensor

from monailabel.transform.cache import CacheTransformDatad, init_cache


class TestInitCache(unittest.TestCase):
    def test_init_cache_idempotent(self):
        # Should not raise and should be safe to call repeatedly.
        init_cache()
        init_cache()


class TestCacheTransformDatad(unittest.TestCase):
    def test_save_and_load_keyed_in_memory(self):
        t = CacheTransformDatad(keys=["pred"], hash_key=["img_path", "model"], in_memory=True)
        data = {"img_path": "/tmp/img_a.nii.gz", "model": "segmentation", "pred": torch.tensor([1.0, 2.0, 3.0])}

        out = t(data)  # __call__ -> save
        self.assertIn("pred", out)

        loaded = t.load({"img_path": "/tmp/img_a.nii.gz", "model": "segmentation"})
        self.assertIsNotNone(loaded)
        self.assertTrue(torch.equal(loaded["pred"], torch.tensor([1.0, 2.0, 3.0])))

    def test_load_miss_returns_none(self):
        t = CacheTransformDatad(keys=["pred"], hash_key=["img_path", "model"], in_memory=True)
        loaded = t.load({"img_path": "/tmp/does_not_exist.nii.gz", "model": "nope-unique-xyz"})
        self.assertIsNone(loaded)

    def test_full_dict_cache_no_keys(self):
        t = CacheTransformDatad(keys=[], hash_key="img_path", in_memory=True)
        data = {"img_path": "/tmp/full_dict_key.nii.gz", "a": 1, "b": "two"}
        t.save(data)
        loaded = t.load({"img_path": "/tmp/full_dict_key.nii.gz"})
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["a"], 1)
        self.assertEqual(loaded["b"], "two")

    def test_save_missing_hash_key_is_noop(self):
        # hash key value missing -> caching skipped, data returned unchanged
        t = CacheTransformDatad(keys=["pred"], hash_key=["img_path", "model"], in_memory=True)
        data = {"img_path": "/tmp/only_one_key.nii.gz", "pred": torch.tensor([9.0])}  # no "model"
        out = t.save(data)
        self.assertIn("pred", out)
        # since caching was skipped, a subsequent load should miss
        loaded = t.load({"img_path": "/tmp/only_one_key.nii.gz", "model": ""})
        self.assertIsNone(loaded)

    def test_metatensor_applied_operations_id_reset(self):
        t = CacheTransformDatad(keys=["pred"], hash_key=["img_path", "model"], in_memory=True)
        mt = MetaTensor(torch.tensor([1.0, 2.0]))
        mt.applied_operations = [{"id": "abc"}]
        t.save({"img_path": "/tmp/meta_key.nii.gz", "model": "m", "pred": mt})
        loaded = t.load({"img_path": "/tmp/meta_key.nii.gz", "model": "m"})
        self.assertIsNotNone(loaded)
        for o in loaded["pred"].applied_operations:
            self.assertEqual(o["id"], "none")

    def test_str_hash_key_normalized_to_list(self):
        t = CacheTransformDatad(keys=["pred"], hash_key="img_path", in_memory=True)
        self.assertEqual(t.hash_key, ["img_path"])


if __name__ == "__main__":
    unittest.main()
