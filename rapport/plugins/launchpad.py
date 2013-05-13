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
