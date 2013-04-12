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
import site
import sys

import jinja2


def _get_template_dirs(type="plugin"):
    """Return a list of directories where templates may be located.
    """
    template_dirs = [
        os.path.expanduser(os.path.join("~", ".rapport", "templates", type)),
        os.path.join("rapport", "templates", type)  # Local dev tree
    ]  + map(lambda d: os.path.join(d, "rapport", "templates", type), site.getsitepackages())
    return template_dirs


_JINJA2_ENV = {}
def init():
    for type in ["plugin", "email", "web"]:
        loader = jinja2.FileSystemLoader(_get_template_dirs(type))
        env = jinja2.Environment(loader=loader,
                                 extensions=["jinja2.ext.i18n"],
                                 trim_blocks=True)
        env.install_null_translations(newstyle=False)
        _JINJA2_ENV[type] = env


def get_template(name, format="text", type="plugin"):
    if not _JINJA2_ENV:
        init()
    template_name = "{0}.{1}.jinja2".format(name, format)
    try:
        return _JINJA2_ENV[type].get_template(template_name)
    except jinja2.TemplateNotFound as e:
        print >>sys.stderr, "Missing template {0}/{1}!".format(type, template_name)

