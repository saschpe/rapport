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
Launchpad plugin.
"""

import warnings

warnings.filterwarnings('ignore', 'Module argparse was already imported')   # Filter a UserWarning from Jinja2
from launchpadlib.launchpad import Launchpad

import rapport.plugin


class LaunchpadPlugin(rapport.plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(LaunchpadPlugin, self).__init__(*args, **kwargs)

        self.lp = Launchpad.login_anonymously(self.login, 'production')

    def _get_json(url):
        return json.loads(requests.get(url).text)

    def collect(self, timeframe):
        bug_tasks = self.lp.people["saschpe"].searchTasks()

        #TODO: Try to find some useful info
        return self._results()


rapport.plugin.register("launchpad", LaunchpadPlugin)
