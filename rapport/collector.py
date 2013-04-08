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

import urlparse

from rapport.util import camelcase_to_underscores
from rapport.plugin import RapportPlugin


class Collector(RapportPlugin):
    """
    """

    def __init__(self, alias=None, url=None, login=None, password=None):
        self.alias = alias
        self.url = url
        self.login = login
        self.password = password

        if alias == "":
            self.alias == self.__str__()

        if url and type(url) is not urlparse.ParseResult:
            self.url = urlparse.urlparse(url)

    def _results(self, dict={}):
        """Helper to merge a dict with cross-collector defaults.

        All collector sub-classes share some config values, i.e.  alias, url,
        login and password. This help should be used in the :collect: method
        of any Collector implementation.

           >>> from rapport import collector
           >>> c = collector.Collector(alias="a", url="http://example.com", login="u")
           >>> c._results()
           {'url': 'http://example.com', 'alias': 'a', 'login': 'u'}
           >>> c._results({'mykey': 'mykey'})
           {'url': 'http://example.com', 'alias': 'a', 'login': 'u', 'mykey': 'mykey'}
        """
        results = {"alias": self.alias,
                   "url": self.url.geturl(),
                   "login": self.login}.copy()
        results.update(dict)
        return results

    def __str__(self):
        """Returns the class name in underscores.

        Additionally, for sub-classes, the suffix '_collector' is split off.

            >>> from rapport import collector
            >>> c = collector.Collector()
            >>> str(c)
            'collector'
        """
        return camelcase_to_underscores(self.__class__.__name__) \
            .rsplit("_collector")[0]

    def collect(self, timeframe):
        """
        """
        raise NotImplementedError()
