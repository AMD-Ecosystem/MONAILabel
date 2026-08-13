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

import numpy as np
import torch
from monai.data import MetaTensor

from monailabel.scribbles.transforms import InteractiveSegmentationTransform, SoftenProbSoftmax


class _ConcreteIST(InteractiveSegmentationTransform):
    # InteractiveSegmentationTransform is abstract (MONAI Transform requires
    # __call__); provide a trivial concrete impl to exercise the inherited helpers.
    def __call__(self, data):
        return data


class TestInteractiveSegmentationTransformHelpers(unittest.TestCase):
    def setUp(self):
        self.t = _ConcreteIST()

    def test_fetch_data_missing_key_raises(self):
        with self.assertRaises(ValueError):
            self.t._fetch_data({"a": np.zeros(2)}, "missing")

    def test_fetch_data_ndarray_copy(self):
        arr = np.ones((2, 2))
        out = self.t._fetch_data({"x": arr}, "x")
        self.assertTrue(np.array_equal(out, arr))
        out[0, 0] = 99  # ensure it's a copy
        self.assertEqual(arr[0, 0], 1)

    def test_fetch_data_metatensor(self):
        mt = MetaTensor(torch.ones(2, 2))
        out = self.t._fetch_data({"x": mt}, "x")
        self.assertEqual(out.shape, (2, 2))

    def test_save_data_plain(self):
        d = self.t._save_data({}, "k", np.zeros(3))
        self.assertIn("k", d)

    def test_save_data_into_metatensor(self):
        mt = MetaTensor(torch.zeros(2, 2))
        d = {"k": mt}
        new_val = np.ones((2, 2))
        out = self.t._save_data(d, "k", new_val)
        self.assertTrue(np.array_equal(out["k"].array, new_val))

    def test_normalise_logits_already_prob(self):
        # columns sum to 1 already -> unchanged
        data = np.array([[0.5, 0.2], [0.5, 0.8]])
        out = self.t._normalise_logits(data, axis=0)
        self.assertTrue(np.allclose(np.sum(out, axis=0), 1.0))

    def test_normalise_logits_applies_softmax(self):
        data = np.array([[2.0, 1.0], [0.5, 3.0]])  # not normalized
        out = self.t._normalise_logits(data, axis=0)
        self.assertTrue(np.allclose(np.sum(out, axis=0), 1.0))

    def test_copy_affine_present(self):
        d = {"logits_meta_dict": {"affine": np.eye(4)}}
        out = self.t._copy_affine(d, "logits", "prob")
        self.assertIn("prob_meta_dict", out)
        self.assertTrue(np.array_equal(out["prob_meta_dict"]["affine"], np.eye(4)))

    def test_copy_affine_absent_noop(self):
        d = {"foo": 1}
        out = self.t._copy_affine(d, "logits", "prob")
        self.assertNotIn("prob_meta_dict", out)

    def test_set_scribbles_idx_from_labelinfo(self):
        self.t.scribbles_bg_label = 2
        self.t.scribbles_fg_label = 3
        d = {
            "label_info": [
                {"name": "background_scribbles", "id": 7},
                {"name": "foreground_scribbles", "id": 8},
            ]
        }
        self.t._set_scribbles_idx_from_labelinfo(d)
        self.assertEqual(self.t.scribbles_bg_label, 7)
        self.assertEqual(self.t.scribbles_fg_label, 8)


class TestSoftenProbSoftmax(unittest.TestCase):
    def test_call_produces_prob(self):
        t = SoftenProbSoftmax(logits="logits", prob="prob")
        logits = np.zeros((2, 4, 4), dtype=np.float32)
        logits[1, ...] = 1.0
        out = t({"logits": logits})
        self.assertIn("prob", out)
        # softmax over axis 0 -> channels sum to ~1
        self.assertTrue(np.allclose(np.sum(out["prob"], axis=0), 1.0, atol=1e-5))


if __name__ == "__main__":
    unittest.main()
