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
Gerrit plugin.
"""

from __future__ import print_function

import json
from datetime import datetime

import paramiko

import rapport.plugin


class GerritPlugin(rapport.plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(GerritPlugin, self).__init__(*args, **kwargs)

        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()

    def _ssh_cmd(self, *args):
        """Execute a gerrit command over SSH.
        """
        command = "gerrit {0}".format(" ".join(args))
        _, stdout, stderr = self._client.exec_command(command)
        return (stdout.readlines(), stderr.readlines())

    def _ssh_query(self, *args):
        """Execute a gerrit query over SSH and returns JSON-formatted data.
        """
        return self._ssh_cmd("query", "--format=JSON", *args)

    def collect(self, timeframe):
        self._client.connect(self.url.hostname, self.url.port, self.login)
        stdout, stderr = self._ssh_query("owner:{0}".format(self.login))
        self._client.close()

        changes = []
        if not stderr:
            for line in stdout[:-1]:  # Last line contains only download stats
                change = json.loads(line)
                if "lastUpdated" in change:
                    last_updated = datetime.utcfromtimestamp(
                        change["lastUpdated"])
                    if timeframe.contains(last_updated):
                        changes.append(change)
                else:
                    print("Change {0} is missing lastUpdated".format(change))

        return self._results({"changes": changes})


rapport.plugin.register("gerrit", GerritPlugin)
