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

# Custom hack for running rapport/cli inside the development tree:
if __name__ == "__main__":
    sys.path.append(os.getcwd())

import rapport
import rapport.config
import rapport.plugin


class RapportCLI(object):
    def __init__(self):
        rapport.plugin.discover()
        rapport.config.configure()

        self.plugins = []
        for plugin in rapport.config.plugins():
            self.plugins.append(rapport.plugin.init(**plugin))

    def _collect(self):

       #timeframe = CurrentWeekTimeframe()

       #gc = GerritCollector(alias="roo",
       #                     url="ssh://review.openstack.org:29418",
       #                     login="saschpe")

       #bnc = BugzillaCollector(alias="bnc",
       #                        url="https://bugzilla.novell.com",
       #                        login="saschpe",
       #                        password="wioX9qud")

       #collectors = []
       #print gc.collect(timeframe)
       #for plugin in plugins:
       #    result_json = plugin.collect()
       #    print result_json
        pass

    def _generate(self):
        pass

    def _edit(self):
        pass

    def _send(self):
        pass

    def main(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version",
                            version="rapport {0}".format(rapport.__version__))
        subparsers = parser.add_subparsers(title="commands")

        parser_collect = subparsers.add_parser("collect", help="collect activities from various sources")
        parser_collect.add_argument("source", nargs="?", help="specific source")
        parser_collect.set_defaults(func=self._collect)

       #parser_generate = subparsers.add_parser("generate", help="generate template from collected data")
       ##parser_generate.add_argument("source", nargs="?", help="specific source")
       ##parser_create.add_argument("-t", "--type", default="text", nargs="?", help="work report type (text, html)")
       #parser_generate.set_defaults(func=self._generate)

       #parser_edit = subparsers.add_parser("edit", help="edit report prior to sending")
       #parser_edit.set_defaults(func=self._edit)

       #parser_send = subparsers.add_parser("send", help="send work report")
       ##parser_generate.add_argument("destination", nargs="+", help="")
       #parser_send.set_defaults(func=self._send)

       #parser_help = subparsers.add_parser("help", help="show this help")
       #parser_help.set_defaults(func=lambda args: parser.print_help())

        args = parser.parse_args()
        args.func(args)


def main():
   #try:
        RapportCLI().main(sys.argv[1:])
   #except Exception as e:
   #    print >> sys.stderr, e
   #    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
