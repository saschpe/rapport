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
import ConfigParser


def _get_config_dirs():
    """Return a list of directories where config files may be located.

    The following directories are returned::

      ~/.rapport/
      /etc/rapport/
    """
    config_dirs = [
        os.path.expanduser(os.path.join("~", ".rapport")),
        os.path.join("etc", "rapport"),
        os.path.abspath(".")
    ]
    return config_dirs


def _get_plugin_dirs():
    """Return a list of directories where plugins may be located.
    """
    return map(lambda d: os.path.join(d, "plugins"), _get_config_dirs())


def _get_template_dirs():
    """Return a list of directories where templates may be located.
    """
    return map(lambda d: os.path.join(d, "templates"), _get_config_dirs())
    return template_dirs


def find_config_files():
    """Return a list of default configuration files.
    """
    config_files = []

    for config_dir in _get_config_dirs():
        path = os.path.join(config_dir, "rapport.conf")
        if os.path.exists(path):
            config_files.append(path)

    return filter(bool, config_files)


def find_plugin_files():
    """Return a list of rapport plugin files.
    """
    plugin_files = []

    for plugin_dir in _get_plugin_dirs():
        if os.path.isdir(plugin_dir):
            for plugin_file in os.listdir(plugin_dir):
                if plugin_file.endswith(".py"):
                    plugin_files.append(os.path.join(plugin_dir, plugin_file))

    return filter(bool, plugin_files)
