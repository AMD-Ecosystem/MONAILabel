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
#
# Modifications Copyright (C) 2026 Advanced Micro Devices, Inc. All rights reserved.

import os
import unittest

import monailabel
from .context import BasicEndpointTestSuite


class TestEndPointLogs(BasicEndpointTestSuite):
    def test_ohif(self):
        response = self.client.get("/ohif/")
        # When the OHIF plugin is built (BUILD_OHIF=true) the static viewer is
        # bundled and served (200); otherwise the endpoint returns 404.
        ohif_index = os.path.join(
            os.path.dirname(monailabel.__file__), "endpoints", "static", "ohif", "index.html"
        )
        if os.path.exists(ohif_index):
            assert response.status_code == 200
        else:
            assert response.status_code == 404


if __name__ == "__main__":
    unittest.main()
