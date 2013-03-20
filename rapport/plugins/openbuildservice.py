#
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
Collector for Open Build Service activities.
"""

import lxml.etree
import requests

from rapport.plugin import CollectorPlugin


class OpenBuildServiceCollector(CollectorPlugin):
    def __init__(self, *args, **kwargs):
        super(OpenBuildServiceCollector, self).__init__(*args, **kwargs)
        self.obs_api_url = "https://api.opensuse.org"
        self.obs_user = "saschpe"
        self.obs_password = "wioX9qud"

    def _get_xml(self, url):
        response = requests.get(url, auth=(self.obs_user, self.obs_password))
        return lxml.etree.fromstring(reponse.text)

    def collect(self):
        # Directly querying for all user's requests is killing the OBS api.
        # So we ask for all projects / packages where the user is involved in first.

        user_projects_url = "{0}/search/project/id?match=person/@userid='{1}'".format(obs_api_url, obs_user)
        xml_root = self._get_xml(user_projects_url)
        user_projects = [project.get('name') for project in xml_root.iterfind(".//project")]

        #user_packages_url = "{0}/search/package/id?match=person/@userid='{1}'".format(obs_api_url, obs_user)
        #xml_root = self._get_xml(user_projects_url)
        #user_packages = [package.values() for package in xml_root.iterfind(".//package")]

        #"https://api.opensuse.org/search/request/id?match=history/@who='saschpe'"

        for project in user_projects:
            requests = self._get_xml("{0}/request?view=collection&user={1}&project={2}".format(obs_api_url, obs_user, project))
