# Copyright (c) 2013, Sascha Peilicke <saschpe@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA


import os
import unittest

from rapport import config


class ConfigTestCase(unittest.TestCase):
    def test__get_config_dirs(self):
        config_dirs = config._get_config_dirs()
        self.assertIn(os.path.expanduser(os.path.join("~", ".rapport")), config_dirs)
        self.assertIn(os.path.join("etc", "rapport"), config_dirs)
        self.assertIn(os.path.abspath("."), config_dirs)

    def test__get_plugin_dirs(self):
        plugin_dirs = config._get_plugin_dirs()
        self.assertIn(os.path.expanduser(os.path.join("~", ".rapport", "plugins")), plugin_dirs)
        self.assertIn(os.path.join("etc", "rapport", "plugins"), plugin_dirs)
        self.assertIn(os.path.abspath("plugins"), plugin_dirs)

    def test__get_template_dirs(self):
        template_dirs = config._get_template_dirs()
        self.assertIn(os.path.expanduser(os.path.join("~", ".rapport", "templates")), template_dirs)
        self.assertIn(os.path.join("etc", "rapport", "templates"), template_dirs)
        self.assertIn(os.path.abspath("templates"), template_dirs)
