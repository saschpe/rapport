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
Gerrit plugin.
"""

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
