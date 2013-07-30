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
Open Build Service plugin.
"""

import lxml.etree
import requests

import rapport.plugin


class OpenBuildServicePlugin(rapport.plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(OpenBuildServicePlugin, self).__init__(*args, **kwargs)

    def _get_xml(self, url):
        response = requests.get(url, auth=(self.login, self.password))
        return lxml.etree.fromstring(response.text)

    def collect(self, timeframe):
        # Directly querying for all user's requests is killing the OBS api.
        # So we ask for all projects / packages where the user is involved in first.

        user_projects_url = "{0}/search/project/id?match=person/@userid='{1}'".format(self.url.geturl(), self.login)
        xml_root = self._get_xml(user_projects_url)
        user_projects = [project.get('name') for project in xml_root.iterfind(".//project")]

        #user_packages_url = "{0}/search/package/id?match=person/@userid='{1}'".format(self.url.geturl(), self.login)
        #xml_root = self._get_xml(user_projects_url)
        #user_packages = [package.values() for package in xml_root.iterfind(".//package")]

        #"https://api.opensuse.org/search/request/id?match=history/@who='saschpe'"

        for project in user_projects:
            #requests = self._get_xml("{0}/request?view=collection&user={1}&project={2}".format(self.url.geturl(), self.login, project))
            pass


rapport.plugin.register("openbuildservice", OpenBuildServicePlugin)
