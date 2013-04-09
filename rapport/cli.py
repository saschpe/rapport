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
if sys.version_info > (3, 3):
    import concurrent.futures as futures
else:
    import futures

# Custom hack for running rapport/cli inside the development tree:
if __name__ == "__main__":
    sys.path.append(os.getcwd())

import rapport
import rapport.config
import rapport.plugin
import rapport.timeframe


rapport.config.load()
rapport.plugin.discover()


class CLI(object):
    def __init__(self):
        self.plugins = rapport.plugin.init_from_config()
        self.timeframe = rapport.timeframe.init_from_config()

    def collect(self):
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
           fs = dict((executor.submit(p.collect, self.timeframe), p.alias) for p in self.plugins)
           for future in futures.as_completed(fs):
               print "Result for {0}: {1}".format(fs[future], future.result())

    def generate(self):
        pass

    def edit(self):
        pass

    def send(self):
        pass

    def main(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version",
                            version="rapport {0}".format(rapport.__version__))
        #parser.add_argument('--verbose', '-v', action='count')

        subparsers = parser.add_subparsers(title="commands")

        parser_collect = subparsers.add_parser("collect", help="collect activities from various sources")
        parser_collect.add_argument("source", nargs="?", help="specific source")
        parser_collect.set_defaults(func=CLI.collect(self))

       #parser_generate = subparsers.add_parser("generate", help="generate template from collected data")
       ##parser_generate.add_argument("source", nargs="?", help="specific source")
       ##parser_create.add_argument("-t", "--type", default="text", nargs="?", help="work report type (text, html)")
       #parser_generate.set_defaults(func=CLI.generate(self))

       #parser_edit = subparsers.add_parser("edit", help="edit report prior to sending")
       #parser_edit.set_defaults(func=CLI.edit(self))

       #parser_send = subparsers.add_parser("send", help="send work report")
       ##parser_generate.add_argument("destination", nargs="+", help="")
       #parser_send.set_defaults(func=CLI.send(self))

        parser_help = subparsers.add_parser("help", help="show this help")
        parser_help.set_defaults(func=lambda args: parser.print_help())

        args = parser.parse_args()


def main():
   #try:
        CLI().main(sys.argv[1:])
   #except Exception as e:
   #    print >> sys.stderr, e
   #    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
