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

from monailabel.tasks.train.utils import from_engine_idx, region_wise_metrics, region_wise_rmse


class TestRegionWiseMetrics(unittest.TestCase):
    def test_no_regions(self):
        m = region_wise_metrics(regions=None, metric="val_mean_dice", prefix="val")
        self.assertIn("val_mean_dice", m)
        self.assertEqual(len(m), 1)

    def test_regions_as_dict(self):
        m = region_wise_metrics(regions={"spleen": 1, "liver": 2}, metric="val_mean_dice", prefix="val")
        self.assertIn("val_mean_dice", m)
        self.assertIn("val_spleen_mean_dice", m)
        self.assertIn("val_liver_mean_dice", m)

    def test_regions_as_sequence(self):
        m = region_wise_metrics(regions=["spleen", "liver"], metric="val_mean_dice", prefix="val")
        # sequence -> enumerated starting at 1
        self.assertIn("val_spleen_mean_dice", m)
        self.assertIn("val_liver_mean_dice", m)


class TestRegionWiseRmse(unittest.TestCase):
    def test_no_regions(self):
        m = region_wise_rmse(regions=None, metric="val_rmse", prefix="val")
        self.assertIn("val_rmse", m)
        self.assertEqual(len(m), 1)

    def test_regions(self):
        m = region_wise_rmse(regions={"a": 1}, metric="val_rmse", prefix="val")
        self.assertIn("val_rmse", m)
        self.assertIn("val_a_rmse", m)


class TestFromEngineIdx(unittest.TestCase):
    def _sample(self):
        # pred/label each a list of one [C, H, W] tensor with 3 channels
        pred = [torch.rand(3, 2, 2)]
        label = [torch.rand(3, 2, 2)]
        return pred, label

    def test_dict_input(self):
        pred, label = self._sample()
        wrapper = from_engine_idx(["pred", "label"], idx=1)
        p_n, l_n = wrapper({"pred": pred, "label": label})
        # each returned entry keeps channel dim of size 1 at front
        self.assertEqual(p_n[0].shape[0], 1)
        self.assertEqual(l_n[0].shape[0], 1)

    def test_list_of_dicts_input(self):
        pred, label = self._sample()
        wrapper = from_engine_idx(["pred", "label"], idx=0)
        data = [{"pred": pred[0], "label": label[0]}]
        p_n, l_n = wrapper(data)
        self.assertEqual(p_n[0].shape[0], 1)
        self.assertEqual(l_n[0].shape[0], 1)


if __name__ == "__main__":
    unittest.main()
