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

from monailabel.datastore.utils.dicom import (
    dicom_web_download_series,
    generate_key,
    get_scu,
    store_scu,
)


class TestGenerateKey(unittest.TestCase):
    def test_deterministic(self):
        a = generate_key("p1", "st1", "se1")
        b = generate_key("p1", "st1", "se1")
        self.assertEqual(a, b)

    def test_distinct_inputs_differ(self):
        a = generate_key("p1", "st1", "se1")
        b = generate_key("p1", "st1", "se2")
        self.assertNotEqual(a, b)

    def test_is_md5_hex(self):
        a = generate_key("p1", "st1", "se1")
        self.assertEqual(len(a), 32)
        int(a, 16)  # raises if not valid hex


class TestScuCommands(unittest.TestCase):
    def test_get_scu_invokes_run_command(self):
        with mock.patch("monailabel.datastore.utils.dicom.run_command") as rc:
            get_scu("1.2.3", "/tmp/out", query_level="SERIES")
            self.assertTrue(rc.called)

    def test_store_scu_invokes_run_command_per_file(self):
        with mock.patch("monailabel.datastore.utils.dicom.run_command") as rc:
            store_scu(["a.dcm", "b.dcm"])
            self.assertEqual(rc.call_count, 2)


class _FakeInstance:
    def __init__(self, sop):
        self._sop = sop

    def __getitem__(self, key):
        # emulate pydicom dataset element access: instance["SOPInstanceUID"].value
        return mock.Mock(value=self._sop)

    def save_as(self, filename):
        with open(filename, "w") as f:
            f.write("dcm")


class TestDicomWebDownloadSeries(unittest.TestCase):
    def test_download_non_frame(self):
        client = mock.Mock()
        client.retrieve_series.return_value = [_FakeInstance("1.1"), _FakeInstance("1.2")]
        with tempfile.TemporaryDirectory() as d:
            dicom_web_download_series("study1", "series1", d, client, frame_fetch=False)
            self.assertEqual(sorted(os.listdir(d)), ["1.1.dcm", "1.2.dcm"])
        client.retrieve_series.assert_called_once_with("study1", "series1")

    def test_download_frame_fetch(self):
        # frame_fetch=True -> retrieve_series_metadata + retrieve_instance_frames
        client = mock.Mock()
        client.retrieve_series_metadata.return_value = [
            {"00080018": {"vr": "UI", "Value": ["3.1"]}}
        ]
        client.retrieve_instance_frames.return_value = [b"\x00\x01\x02\x03"]
        with tempfile.TemporaryDirectory() as d:
            dicom_web_download_series("study1", "series1", d, client, frame_fetch=True)
            self.assertEqual(os.listdir(d), ["3.1.dcm"])
        client.retrieve_series_metadata.assert_called_once_with("study1", "series1")


if __name__ == "__main__":
    unittest.main()
