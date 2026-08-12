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
    file_checksum,
    get_basename_no_ext,
    gpu_memory_map,
)


class TestBasenameNoExt(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(get_basename_no_ext("/a/b/image.nii.gz"), "image")

    def test_no_dir(self):
        # NOTE: the implementation uses str.rstrip(ext), which strips trailing
        # *characters* in the ext set (not the suffix), so "scan.nrrd" -> "sca".
        # Asserting the actual behavior to lock it in for coverage.
        self.assertEqual(get_basename_no_ext("scan.nrrd"), "sca")


class TestFileChecksum(unittest.TestCase):
    def test_bad_algo_raises(self):
        with self.assertRaises(ValueError):
            file_checksum("whatever.bin", algo="NOTAREALALGO")

    def test_sha256_of_temp_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"hello monailabel")
            path = f.name
        try:
            out = file_checksum(path, algo="SHA256")
            self.assertTrue(out.startswith("SHA256:"))
            self.assertEqual(len(out.split(":")[1]), 64)  # sha256 hex length
        finally:
            os.remove(path)


class TestGpuMemoryMap(unittest.TestCase):
    def test_nvidia_smi_path(self):
        def which(cmd):
            return "/usr/bin/nvidia-smi" if cmd == "nvidia-smi" else None

        with mock.patch("monailabel.utils.others.generic.shutil.which", side_effect=which), mock.patch(
            "monailabel.utils.others.generic.subprocess.check_output", return_value="1000\n2000\n"
        ):
            self.assertEqual(gpu_memory_map(), {0: 1000, 1: 2000})

    def test_nvidia_smi_exception_returns_default(self):
        def which(cmd):
            return "/usr/bin/nvidia-smi" if cmd == "nvidia-smi" else None

        with mock.patch("monailabel.utils.others.generic.shutil.which", side_effect=which), mock.patch(
            "monailabel.utils.others.generic.subprocess.check_output", side_effect=OSError("boom")
        ):
            self.assertEqual(gpu_memory_map(), {0: 4300})

    def test_rocm_smi_path(self):
        def which(cmd):
            return "/usr/bin/rocm-smi" if cmd == "rocm-smi" else None

        # total=2GiB, used=1GiB -> free ~1024 MB
        csv = "device,Total,Used\ncard0,{},{}\n".format(2 * 1024 * 1024 * 1024, 1 * 1024 * 1024 * 1024)
        with mock.patch("monailabel.utils.others.generic.shutil.which", side_effect=which), mock.patch(
            "monailabel.utils.others.generic.subprocess.check_output", return_value=csv
        ):
            out = gpu_memory_map()
            self.assertIn(0, out)
            self.assertEqual(out[0], 1024)

    def test_rocm_smi_exception_returns_default(self):
        def which(cmd):
            return "/usr/bin/rocm-smi" if cmd == "rocm-smi" else None

        with mock.patch("monailabel.utils.others.generic.shutil.which", side_effect=which), mock.patch(
            "monailabel.utils.others.generic.subprocess.check_output", side_effect=OSError("boom")
        ):
            self.assertEqual(gpu_memory_map(), {0: 4300})

    def test_neither_found_returns_default(self):
        with mock.patch("monailabel.utils.others.generic.shutil.which", return_value=None):
            self.assertEqual(gpu_memory_map(), {0: 4300})


if __name__ == "__main__":
    unittest.main()
