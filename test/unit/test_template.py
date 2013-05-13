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

import rapport.template


class TemplateTestCase(unittest.TestCase):
    def test__get_template_dirs(self):
        for type in ["plugin", "email", "web"]:
            template_dirs = rapport.template._get_template_dirs(type)
            self.assertIn(os.path.expanduser(os.path.join("~", ".rapport", "templates", type)), template_dirs)
            self.assertIn(os.path.join("rapport", "templates", type), template_dirs)
