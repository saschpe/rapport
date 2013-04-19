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
Command-line interface to rapport.
"""

import argparse
import getpass
import os
import sys

import rapport
import rapport.config
import rapport.email
import rapport.plugin
import rapport.report
import rapport.timeframe


rapport.config.load()
rapport.config.init_user()
rapport.plugin.discover()


class CLI(object):
    def __init__(self):
        self.plugins = rapport.plugin.init_from_config()
        self.timeframe = rapport.timeframe.init_from_config()

    def create(self, args):
        report = rapport.report.create_report(self.plugins, self.timeframe)
        print "Your work report for {0}:\n{1}".format(self.timeframe, report["body"])

    def list(self, args):
        for report in rapport.report.list_reports():
            print report

    def show(self, args):
        report = rapport.report.get_report(args.report)
        if args.raw:
            print report
        else:
            print report["email.body.text"]

    def delete(self, args):
        for report in args.report:
            rapport.report.delete_report(report)


   #def edit(self, args):
   #    pass

   #def email_send(self, args):
   #    pass

   #def email_compose(self, args):
   #    pass

    def email_xdg(self, args):
        report = rapport.report.get_report(args.report)
        rapport.email.xdg_compose(to=rapport.config.get("email", "to"),
                                  subject=report["email.subject.text"],
                                  body=report["email.body.text"],
                                  cc=rapport.config.get("email", "cc"),
                                  bcc=rapport.config.get("email", "bcc"))

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-V", "--version", action="version", version="rapport {0}".format(rapport.__version__))
        parser.add_argument("-v", "--verbosity", action="count", help="verbosity level (-v or -vv)")
        subparsers = parser.add_subparsers(title="commands")

        parser_create = subparsers.add_parser("create", help="create a new work report")
        parser_create.set_defaults(func=self.create)
        parser_list = subparsers.add_parser("list", help="list already existing work reports")
        parser_list.set_defaults(func=self.list)
        parser_show = subparsers.add_parser("show", help="display a specific work report")
        parser_show.add_argument("-r", "--raw", action="store_true", help="display the raw report data")
        parser_show.add_argument("report", nargs="?", default=None)
        parser_show.set_defaults(func=self.show)
        parser_delete = subparsers.add_parser("delete", help="delete a work report")
        parser_delete.add_argument("report", nargs="+", help="the report to delete")
        parser_delete.set_defaults(func=self.delete)
       #parser_edit = subparsers.add_parser("edit", help="edit report prior to sending")
       #parser_edit.set_defaults(func=self.edit)

        parser_email = subparsers.add_parser("email", help="e-mail composing and sending")
        email_subparsers = parser_email.add_subparsers(title="e-mail commands")
       #parser_email_send = email_subparsers.add_parser("send")
       #parser_email_send.set_defaults(func=self.email_send)
       #parser_email_compose = email_subparsers.add_parser("compose")
       #parser_email_compose.set_defaults(func=self.email_compose)
        parser_email_xdg = email_subparsers.add_parser("xdg", help="use xdg-email to compose, i.e. use your preferred mailer under KDE/GNOME/XFCE/etc.")
        parser_email_xdg.add_argument("report", nargs="?", default=None)
        parser_email_xdg.set_defaults(func=self.email_xdg)
        parser_email_help = email_subparsers.add_parser("help", help="show e-mail help")
        parser_email_help.set_defaults(func=lambda args: parser_email.print_help())

        parser_help = subparsers.add_parser("help", help="show this help")
        parser_help.set_defaults(func=lambda args: parser.print_help())

        args = parser.parse_args()
        args.func(args)

        #TODO: This is beginning to look ugly. Maybe use oslo.config or sth.:
        if args.verbosity > rapport.config.get_int("rapport", "verbosity"):
            rapport.config.set("rapport", "verbosity", args.verbosity)


def main():
   #try:
        CLI().main()
   #except Exception as e:
   #    print >> sys.stderr, e
   #    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
