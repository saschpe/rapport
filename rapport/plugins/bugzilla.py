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
Bugzilla plugin.
"""

# Avoid name clash with global "bugzilla" module from python-bugzilla:
from __future__ import absolute_import
import bugzilla

import rapport.plugin


class BugzillaPlugin(rapport.plugin.Plugin):
    def __init__(self, email, *args, **kwargs):
        super(BugzillaPlugin, self).__init__(*args, **kwargs)
        self.email = email

        self.url = "{0}/xmlrpc.cgi".format(self.url.geturl())

    def collect(self, timeframe):
        bz = bugzilla.Bugzilla(url=self.url)
        bz.login(user=self.login, password=self.password)

        open_bugs = bz.query({"assigned_to": self.email,
                              "bug_status": ["NEW", "ASSIGNED"]})
        closed_bugs = bz.query({"assigned_to": self.email,
                                "bug_status": ["CLOSED", "RESOLVED"],
                                "last_change_time": timeframe.start})

        return self._results({"email": self.email, "open_bugs": open_bugs,
                              "closed_bugs": closed_bugs})


rapport.plugin.register("bugzilla", BugzillaPlugin)
