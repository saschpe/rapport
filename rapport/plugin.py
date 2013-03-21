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

from jinja2 import Environment, PackageLoader

from rapport.period import DefaultPeriod


class Plugin(object):
    template_env = Environment(loader=PackageLoader('rapport', 'templates'))

    def __init__(self, alias=None, *args, **kwargs):
        self.alias = alias

    def collect(self, period=DefaultPeriod()):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()


# TODO: ARgparse stuff

# TODO: template rendere stuff