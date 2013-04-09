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

        url = "{0}/xmlrpc.cgi".format(self.url.geturl())
        self._bz = bugzilla.Bugzilla(url=url)
        self._bz.login(user=self.login, password=self.password)

    def collect(self, timeframe):
        open_bugs = self._bz.query({"assigned_to": self.email,
                                    "bug_status": ["NEW", "ASSIGNED"]})
        closed_bugs = self._bz.query({"assigned_to": self.email,
                                      "bug_status": ["CLOSED", "RESOLVED"],
                                      "last_change_time": timeframe.start})

        return self._results({"email": self.email, "open_bugs": open_bugs,
                              "closed_bugs": closed_bugs})


rapport.plugin.register("bugzilla", BugzillaPlugin)
