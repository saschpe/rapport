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
Mediawiki plugin.
"""

import json

import requests

import rapport.plugin


class MediawikiPlugin(rapport.plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(MediawikiPlugin, self).__init__(*args, **kwargs)

    def _get(self, params={}):
        params.update({"format": "json", "action": "query"})
        response = requests.get(self.url.geturl(), params=params, auth=(self.login, self.password))
        return json.loads(response.text)["query"]

    def collect(self, timeframe):
        #TODO: Check back ugly "UTC" timestamp hack here:
        edits = self._get({"list": "usercontribs",
                                   "ucuser": "{0}".format(self.login),
                                   "ucstart": timeframe.end.isoformat()+"Z",
                                   "ucend": timeframe.start.isoformat()+"Z"})
        return self._results({"edits": edits["usercontribs"]})


rapport.plugin.register("mediawiki", MediawikiPlugin)
