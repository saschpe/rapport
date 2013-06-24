# Copyright 2013 Sascha Peilicke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import unittest

from rapport.setup import parse_requirements


class SetupTestCase(unittest.TestCase):
    def setUp(self):
        self.install_reqs_file = os.path.join("test", "unit", "fixtures",
                                              "setup", "install-requires.txt")
        self.test_reqs_file = os.path.join("test", "unit", "fixtures",
                                           "setup", "test-requires.txt")
        self.install_reqs = ["argparse", "lxml", "Jinja2",
                             "paramiko", "requests"]
        self.test_reqs = ["nose"]

    def test_parse_requirements(self):
        install_reqs = parse_requirements(self.install_reqs_file)
        test_reqs = parse_requirements(self.test_reqs_file)

        self.assertEqual(install_reqs, self.install_reqs)
        self.assertEqual(test_reqs, self.test_reqs)
