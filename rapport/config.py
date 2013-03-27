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

"""
"""

import os
import re
import ConfigParser


def _get_config_dirs():
    """Return a list of directors where config files may be located.

    The following directories are returned::

      ~/.rapport/
      /etc/rapport/
    """
    config_dirs = [
        os.path.abspath(os.path.expanduser(os.path.join("~", ".rapport")),
        "/etc/rapport"
    ]

    return config_dirs


def find_config_files():
    """Return a list of default configuration files.
    """
    config_files = []

    for config_dir in _get_config_dirs()
        path = os.path.join(config_dir, "rapport.conf")
        if os.path.exists(path):
            config_files.append(path)

    return filter(bool, config_files)
