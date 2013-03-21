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

from jinja2 import Environment, PackageLoader


class Collector(object):
    """
    """

    def __init__(self, alias=None, url=None, username=None, password=None):
        self.alias = alias
        self.url = url
        self.username = username
        self.password = password

    def _results(self, dict={}):
        """Helper to merge a dict with cross-collector defaults.

        All collector sub-classes share some config values, i.e.  alias, url,
        username and password. This help should be used in the :collect: method
        of any Collector implementation.

           >>> from rapport.collector import Collector
           >>> c = Collector(alias="a", username="u")
           >>> c._results()
           '{"alias": "a", "username": "u"}'
           >>> c._results({"mykey": "mykey"})
           '{"alias": "a", "mykey": "mykey", "username": "u"}'
        """
        results = {"collector": "gerrit",
                   "alias:": self.alias,
                   "url": self.url.geturl()}.copy()
        results.update(dict)
        return results

    def collect(self, timeframe):
        """
        """
        raise NotImplementedError()

