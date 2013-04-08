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

import glob
import re
import shutil
import subprocess
import sys
from distutils.core import Command


class PEP8Command(Command):
    description = "Run PEP8 with custom options"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.call(["pep8", "--repeat", "--show-source",
                        "--ignore=E501",
                        "--exclude=.venv,.tox,dist,doc", "."])


class CleanupCommand(Command):
    patterns = [".tox", ".venv", "build", "dist", "*.egg-info"]
    description = "Clean up project directory"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for pattern in CleanupCommand.patterns:
            for file in glob.glob(pattern):
                shutil.rmtree(file, ignore_errors=True)


def get_cmdclass():
    """Dictionary of all distutils commands defined in this module.
    """
    return {"cleanup": CleanupCommand,
            "pep8": PEP8Command}


def parse_requirements(requirements_file='requirements.txt'):
    requirements = []
    with open(requirements_file, 'r') as f:
        for line in f:
            # For the requirements list, we need to inject only the portion
            # after egg= so that distutils knows the package it's looking for
            # such as:
            # -e git://github.com/openstack/nova/master#egg=nova
            if re.match(r'\s*-e\s+', line):
                requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',
                                    line))
            # such as:
            # http://github.com/openstack/nova/zipball/master#egg=nova
            elif re.match(r'\s*https?:', line):
                requirements.append(re.sub(r'\s*https?:.*#egg=(.*)$', r'\1',
                                    line))
            # -f lines are for index locations, and don't get used here
            elif re.match(r'\s*-f\s+', line):
                pass
            # -r lines are for including other files, and don't get used here
            elif re.match(r'\s*-r\s+', line):
                pass
            # argparse is part of the standard library starting with 2.7
            # adding it to the requirements list screws distro installs
            elif line == 'argparse' and sys.version_info >= (2, 7):
                pass
            else:
                requirements.append(line.strip())
    return requirements
