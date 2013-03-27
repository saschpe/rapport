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
Command-line interface to the OpenStack Identity API.
"""

import argparse
import getpass
import os
import sys


class RapportCLI(object):
    def __init__(self):
        pass

    def main(self, argv):
        parser = argparse.ArgumentParser()


        from rapport.plugins.gerrit import GerritCollector
        from rapport.plugins.bugzilla import BugzillaCollector
        from rapport.timeframe import CurrentWeekTimeframe

        timeframe = CurrentWeekTimeframe()

        gc = GerritCollector(alias="roo",
                             url="ssh://review.openstack.org:29418",
                             login="saschpe")

        bnc = BugzillaCollector(alias="bnc",
                                url="https://bugzilla.novell.com",
                                login="saschpe",
                                password="wioX9qud")
        print gc.collect(timeframe)


def main():
    try:
        RapportCLI().main(sys.argv[1:])
    except Exception as e:
        print >> sys.stderr, e
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
