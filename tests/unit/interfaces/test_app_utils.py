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

import json
import os
import tempfile
import unittest

from monailabel.interfaces.exception import MONAILabelException
from monailabel.interfaces.utils.app import app_instance, clear_cache, save_result


class TestAppInstance(unittest.TestCase):
    def test_missing_main_py_raises(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(MONAILabelException):
                app_instance(app_dir=d, studies="x", conf={})

    def test_main_py_without_subclass_raises(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "main.py"), "w") as f:
                f.write("x = 1\n")  # no MONAILabelApp subclass
            with self.assertRaises(MONAILabelException):
                app_instance(app_dir=d, studies="x", conf={})


class TestClearCache(unittest.TestCase):
    def test_clear_cache(self):
        # should not raise; empties the apps registry
        clear_cache()


class TestSaveResult(unittest.TestCase):
    def test_save_result_writes_json(self):
        result = {"label": "spleen", "score": 0.9}
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "result.json")
            save_result(result, out)
            with open(out) as f:
                self.assertEqual(json.load(f), result)

    def test_save_result_no_output_is_noop(self):
        # output=None -> just logs, no file
        save_result({"a": 1}, None)


if __name__ == "__main__":
    unittest.main()
