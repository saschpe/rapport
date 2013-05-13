# Copyright 2013 Sascha Peilicke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
                                   "ucstart": timeframe.end.isoformat() + "Z",
                                   "ucend": timeframe.start.isoformat() + "Z"})
        return self._results({"edits": edits["usercontribs"]})


rapport.plugin.register("mediawiki", MediawikiPlugin)
