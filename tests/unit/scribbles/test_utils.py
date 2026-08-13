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

from monailabel.scribbles.utils import (
    get_eps,
    make_histograms,
    make_iseg_unary,
    make_likelihood_image_histogram,
)


class TestGetEps(unittest.TestCase):
    def test_eps_float32(self):
        self.assertGreater(get_eps(np.zeros(1, dtype=np.float32)), 0.0)


class TestMakeIsegUnary(unittest.TestCase):
    def _prob_scrib(self, bg=True, fg=True):
        # single-channel prob [1, 4, 4]; scribbles [1, 4, 4]
        prob = np.full((1, 4, 4), 0.5, dtype=np.float32)
        scrib = np.zeros((1, 4, 4), dtype=np.float32)
        if bg:
            scrib[0, 0, 0] = 2  # bg label
        if fg:
            scrib[0, 3, 3] = 3  # fg label
        return prob, scrib

    def test_basic_unary_shape(self):
        prob, scrib = self._prob_scrib()
        unary = make_iseg_unary(prob, scrib)
        # single-channel prob is unfolded to 2 channels
        self.assertEqual(unary.shape[0], 2)
        self.assertEqual(unary.shape[1:], (4, 4))

    def test_shape_mismatch_raises(self):
        prob = np.full((1, 4, 4), 0.5, dtype=np.float32)
        scrib = np.zeros((1, 3, 3), dtype=np.float32)
        with self.assertRaises(ValueError):
            make_iseg_unary(prob, scrib)

    def test_multi_channel_scribbles_raises(self):
        prob = np.full((1, 4, 4), 0.5, dtype=np.float32)
        scrib = np.zeros((2, 4, 4), dtype=np.float32)
        with self.assertRaises(ValueError):
            make_iseg_unary(prob, scrib)

    def test_no_scribbles_still_returns(self):
        # no bg/fg scribbles -> warning branches, but still returns unary
        prob, scrib = self._prob_scrib(bg=False, fg=False)
        unary = make_iseg_unary(prob, scrib)
        self.assertEqual(unary.shape[0], 2)


class TestMakeHistograms(unittest.TestCase):
    def test_scalar_alpha(self):
        image = np.random.rand(1, 8, 8).astype(np.float32)
        scrib = np.zeros((1, 8, 8), dtype=np.float32)
        scrib[0, 0, 0] = 2
        scrib[0, 7, 7] = 3
        # returns (fg_hist, bg_hist, bin_edges)
        fg_hist, bg_hist, bin_edges = make_histograms(
            image, scrib, scribbles_bg_label=2, scribbles_fg_label=3, alpha_bg=1, alpha_fg=1, bins=16
        )
        self.assertEqual(len(fg_hist), 16)
        self.assertEqual(len(bg_hist), 16)
        self.assertEqual(len(bin_edges), 17)

    def test_bad_alpha_list_length_raises(self):
        image = np.random.rand(1, 8, 8).astype(np.float32)
        scrib = np.zeros((1, 8, 8), dtype=np.float32)
        scrib[0, 0, 0] = 2
        scrib[0, 7, 7] = 3
        with self.assertRaises(ValueError):
            make_histograms(
                image, scrib, scribbles_bg_label=2, scribbles_fg_label=3, alpha_bg=[1, 2, 3], alpha_fg=1, bins=16
            )


class TestMakeLikelihoodImageHistogram(unittest.TestCase):
    def _inputs(self):
        image = np.random.rand(1, 8, 8).astype(np.float32)
        scrib = np.zeros((1, 8, 8), dtype=np.float32)
        scrib[0, 0, 0] = 2  # bg
        scrib[0, 7, 7] = 3  # fg
        return image, scrib

    def test_returns_prob(self):
        image, scrib = self._inputs()
        out = make_likelihood_image_histogram(image, scrib, 2, 3, num_bins=16)
        # concatenated bg/fg prob -> 2 channels
        self.assertEqual(out.shape[0], 2)

    def test_return_label(self):
        image, scrib = self._inputs()
        out = make_likelihood_image_histogram(image, scrib, 2, 3, num_bins=16, return_label=True)
        self.assertEqual(out.shape[0], 1)

    def test_unnormalized_image_is_rescaled(self):
        # values outside [0,1] exercise the rescale branch
        image = (np.random.rand(1, 8, 8).astype(np.float32) * 100.0) - 50.0
        scrib = np.zeros((1, 8, 8), dtype=np.float32)
        scrib[0, 0, 0] = 2
        scrib[0, 7, 7] = 3
        out = make_likelihood_image_histogram(image, scrib, 2, 3, num_bins=16)
        self.assertEqual(out.shape[0], 2)

    def test_torch_tensor_input(self):
        import torch

        image = torch.rand(1, 8, 8)
        scrib = np.zeros((1, 8, 8), dtype=np.float32)
        scrib[0, 0, 0] = 2
        scrib[0, 7, 7] = 3
        out = make_likelihood_image_histogram(image, scrib, 2, 3, num_bins=16)
        self.assertEqual(out.shape[0], 2)


if __name__ == "__main__":
    unittest.main()
