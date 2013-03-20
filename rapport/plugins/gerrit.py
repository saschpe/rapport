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
Plugin for Gerrit activities.
"""

import json
from datetime import datetime, timedelta

import paramiko

from rapport.plugin import Plugin


class Gerrit(Plugin):
    def __init__(self, *args, **kwargs):
        super(Gerrit, self).__init__(*args, **kwargs)

        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()

        #TODO: Move to cfg:
        self.hostname = "review.openstack.org"
        self.port = 29418
        self.username = "saschpe"

        #TODO: Global config or user input:
        self.to_date = datetime.utcnow()
        self.from_date = self.to_date - timedelta(7)

    def _run_ssh_cmd(self, *args):
        _, stdout, stderr = self._client.exec_command("gerrit {0}".format(" ".join(args)))
        return (stdout.readlines(), stderr.readlines())

    def _run_ssh_query(self, *args):
        return self._run_ssh_cmd("query", "--format=JSON", *args)

    def collect(self, period):
        self._client.connect(self.hostname, self.port, self.username)
        stdout, stderr = self._run_ssh_query("owner:{0}".format(self.username))
        self._client.close()

        changes = []
        if not stderr:
            for line in stdout[:-1]:  # Last line contains only download stats
                change = json.loads(line)
                if change.has_key("lastUpdated"):
                    last_updated = datetime.utcfromtimestamp(change["lastUpdated"])
                    if self.from_date < last_updated and last_updated <= self.to_date:
                        changes.append(change)
                else:
                    print("Change {0} is missing lastUpdated".format(change))

        return {"hostname": self.hostname, 
                "user": self.username,
                "changes": changes}

    def render(self):
        results = self.collect()
        template = Plugin.template_env.get_template("gerrit.txt")
        return template.render(results)

