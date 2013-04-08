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
import sys
import unittest

from rapport import __version__
from rapport.util import silent_popen


class CLIFunctionalTestCase(unittest.TestCase):
    def setUp(self):
        self.result = "rapport {0}\n".format(__version__)

    def test_call_rapport_cli(self):
        args = [sys.executable, "rapport/cli.py", "--version"]
        self.assertEqual(silent_popen(args), self.result)

    def test_call_script_wrapper(self):
        args = ["scripts/rapport", "--version"]
        # The script is meant to be with rapport installed, i.e. not
        # from the (development) tree. Thus we have to adjust PYTHONPATH:
        env = os.environ.copy()
        env.update({"PYTHONPATH": "."})
        self.assertEqual(silent_popen(args, env=env), self.result)
