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

import jinja2


def _get_template_dirs():
    """Return a list of directories where templates may be located.
    """
    template_dirs = [
        os.path.expanduser(os.path.join("~", ".rapport", "templates")),
        os.path.join("templates")
    ]  # + map(lambda d: os.path.join(d, "rapport", "templates"), site.getsitepackages())
    return template_dirs


_JINJA2_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(_get_template_dirs()),
                                 trim_blocks=True)


def get_template(plugin, type):
    template_name = "{0}.{1}.jinja2".format(plugin, type)
    try:
        return _JINJA2_ENV.get_template(template_name)
    except jinja2.TemplateNotFound as e:
        print >>sys.stderr, "Missing {0} {1} template!".format(plugin, type)

