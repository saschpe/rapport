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


import unittest

from rapport.setup import parse_requirements


class SetupTestCase(unittest.TestCase):
    def setUp(self):
        self.install_requires_file = "fixtures/requirements.txt"
        self.test_requires_file = "fixtures/requirements.test.txt"

        self.install_requires = ["argparse", "launchpadlib", "lxml", "Jinja2",
                                 "paramiko", "requests"]
        self.test_requires = ["nose"]

    def test_parse_requirements(self):
        install_requires = parse_requirements("requirements.txt")
        install_requires_default = parse_requirements()

        self.assertEqual(install_requires, install_requires_default)
        self.assertEqual(install_requires, self.install_requires)

        test_requires = parse_requirements("requirements.test.txt")

        self.assertEqual(test_requires, self.test_requires)
