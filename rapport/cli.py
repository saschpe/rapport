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
import rapport.template
import rapport.timeframe


rapport.config.load()
rapport.config.init_user()
rapport.plugin.discover()


class CLI(object):
    def __init__(self):
        self.plugins = rapport.plugin.init_from_config()
        self.timeframe = rapport.timeframe.init_from_config()

    def create(self):
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
            plugin_futures = dict((executor.submit(p.collect, self.timeframe), p) for p in self.plugins)
            for future in futures.as_completed(plugin_futures):
                try:
                    if rapport.config.get_int("rapport", "verbosity") >= 1:
                        print "Result for {0}: {1}".format(plugin_futures[future].alias, future.result())
                    template = rapport.template.get_template(plugin_futures[future], "text")
                    if template:
                        print template.render(future.result())
                except Exception as e:
                    print >>sys.stderr, "Failed plugin {0}: {1}!".format(plugin_futures[future], e)


   #def edit(self):
   #    pass

    def main(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action="version", version="rapport {0}".format(rapport.__version__))
        subparsers = parser.add_subparsers(title="commands")

        parser_create = subparsers.add_parser("create", help="create work report")
        parser_create.set_defaults(func=CLI.create(self))

       #parser_edit = subparsers.add_parser("edit", help="edit report prior to sending")
       #parser_edit.set_defaults(func=CLI.edit(self))

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
