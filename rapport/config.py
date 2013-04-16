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
import shutil
import ConfigParser

import rapport.config


def _get_config_dirs():
    """Return a list of directories where config files may be located.

    The following directories are returned::

      ~/.rapport/
      /etc/rapport/
    """
    config_dirs = [
        os.path.expanduser(os.path.join("~", ".rapport")),
        os.path.join("/", "etc", "rapport"),
        os.path.abspath(os.path.join("rapport", "config"))
    ]
    return config_dirs


def find_config_files():
    """Return a list of default configuration files.
    """
    config_files = []

    for config_dir in _get_config_dirs():
        path = os.path.join(config_dir, "rapport.conf")
        if os.path.exists(path):
            config_files.append(path)

    return filter(bool, config_files)


def init_user():
    """Create and populate the ~/.rapport directory tree if it's not existing.

    Doesn't interfere with already existing directories or configuration files.
    """
    user_conf_dir = os.path.expanduser(os.path.join("~", ".rapport"))
    user_conf_file = os.path.join(user_conf_dir, "rapport.conf")

    if not os.path.exists(user_conf_dir):
        if rapport.config.get_int("rapport", "verbosity") >= 1:
            print "Create user directory {0}".format(user_conf_dir)
        os.makedirs(user_conf_dir)
    for subdir in ["plugins", "reports", "templates/plugin", "templates/email", "templates/web"]:
        user_conf_subdir = os.path.join(user_conf_dir, subdir)
        if not os.path.exists(user_conf_subdir):
            if rapport.config.get_int("rapport", "verbosity") >= 1:
                print "Create user directory {0}".format(user_conf_subdir)
            os.makedirs(user_conf_subdir)
        if subdir == "reports" and not (os.stat(user_conf_subdir).st_mode & 0777) == 0700:
            if rapport.config.get_int("rapport", "verbosity") >= 1:
                print "Set secure directory permissions for {0}".format(user_conf_subdir)
            os.chmod(user_conf_subdir, 0700)
    if not os.path.exists(user_conf_file):
        if rapport.config.get_int("rapport", "verbosity") >= 1:
            print "Create user configuration {0}".format(user_conf_file)
        default_config = find_config_files()
        default_config = os.path.abspath(os.path.join("rapport", "config", "rapport.conf"))
        shutil.copyfile(default_config, user_conf_file)
    if not (os.stat(user_conf_file).st_mode & 0777) == 0600:
        if rapport.config.get_int("rapport", "verbosity") >= 1:
            print "Set secure file permissions for {0}".format(user_conf_file)
        os.chmod(user_conf_file, 0600)


CONF = None


def load():
    global CONF
    config = ConfigParser.SafeConfigParser()
    config.read(find_config_files()[0])
    CONF = config
    return CONF


def get(section, option, default=None):
    if CONF.has_option(section, option):
        return CONF.get(section, option)
    else:
        return default


def get_int(section, option, default=None):
    return int(get(section, option, default))


def set(section, option, value):
    CONF.set(section, option, str(value))


def plugins():
    for section in CONF.sections():
        if section.startswith("plugin:"):
            name, alias = section.split(":")[1:]
            plugin = {"name": name, "alias": alias}
            for option in CONF.options(section):
                plugin[option] = CONF.get(section, option)
            yield plugin
