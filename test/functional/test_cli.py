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
import sys
import unittest

from rapport import __version__
from rapport.util import silent_popen


class CLIFunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.result = "{0}\n".format(__version__)

    def test_call_rapport_cli(self):
        args = [sys.executable, "-m", "rapport.cli", "--version"]
        self.assertEqual(silent_popen(args), self.result)

    def test_call_script_wrapper(self):
        args = ["scripts/rapport", "--version"]
        # The script is meant to be with rapport installed, i.e. not
        # from the (development) tree. Thus we have to adjust PYTHONPATH:
        env = os.environ.copy()
        env.update({"PYTHONPATH": "."})
        self.assertEqual(silent_popen(args, env=env), self.result)
