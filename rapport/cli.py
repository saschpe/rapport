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
Command-line interface to rapport.
"""

from __future__ import print_function

import argparse
import datetime
import sys

import rapport
import rapport.config
import rapport.email
import rapport.plugin
import rapport.report
import rapport.timeframe


rapport.config.load()
rapport.plugin.discover()


class RapportHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = "{0}{1}".format(heading[0].upper(), heading[1:])
        super(RapportHelpFormatter, self).start_section(heading)


class CLI(object):
    def __init__(self):
        self.plugins = rapport.plugin.init_from_config()

    def create(self, args):
        if args.start:
            timeframe = rapport.timeframe.init("generic", start=args.start, end=args.end)
        elif args.current_month:
            timeframe = rapport.timeframe.init("current_month")
        elif args.current_week:
            timeframe = rapport.timeframe.init("current_week")
        elif args.week:
            timeframe = rapport.timeframe.init("week", week=args.week)
        elif args.month:
            timeframe = rapport.timeframe.init("month", month=args.month)
        elif args.recent_days:
            timeframe = rapport.timeframe.init("recent_days", days=args.recent_days)
        else:
            timeframe = rapport.timeframe.init_from_config()

        print("Timeframe: {0}".format(timeframe))
        report = rapport.report.create_report(self.plugins, timeframe)
        print("Work report {0}:\n{1}".format(report["date"], report["body"]))

    def list(self, args):
        for report in rapport.report.list_reports():
            print(report)

    def show(self, args):
        report = rapport.report.get_report(args.report)
        if args.raw:
            print(report)
        else:
            print(report["email.body.text"])

    def delete(self, args):
        for report in args.report:
            rapport.report.delete_report(report)

    def edit(self, args):
        rapport.report.edit_report(args.report, args.type)

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
        parser = argparse.ArgumentParser(prog="rapport",
                                         description="Work report generator for the lazy",
                                         epilog="See \"rapport help COMMAND\" for help on a specific command.",
                                         add_help=False,
                                         formatter_class=RapportHelpFormatter)
        parser.add_argument("--version", action="version", version=rapport.__version__,
                            help="Shows program's version and exits")
        parser.add_argument("-v", "--verbosity", action="count", help="Verbosity level (-v or -vv)")
        subparsers = parser.add_subparsers(title="Positional arguments", metavar="<subcommand>")

        parser_list = subparsers.add_parser("list", help="List existing work reports", formatter_class=RapportHelpFormatter)
        parser_list.set_defaults(func=self.list)

        parser_create = subparsers.add_parser("create", help="Create a new work report", formatter_class=RapportHelpFormatter)
        group_timeframe = parser_create.add_argument_group("Optional timeframe", description="Explicitly pick a timeframe in case you don't want to use the default.")
        group_timeframe.add_argument("-cm", "--current-month", action="store_true", help="Current month (until now)")
        group_timeframe.add_argument("-cw", "--current-week", action="store_true", help="Current week (until now)")
        group_timeframe.add_argument("-w", "--week", type=int, help="Week of year [1..52]")
        group_timeframe.add_argument("-m", "--month", type=int, help="Month of year [1..12]")
        group_timeframe.add_argument("-rd", "--recent-days", nargs="?", const=14, type=int, help="Recent days [1..] (default: 14)")
        group_generic_timeframe = parser_create.add_argument_group("Optional generic timeframe", description="Use in case the standard timeframes don't suit your needs. You can utilize 'date --iso-8601=seconds --utc' to get a date in UTC conforming to ISO 8601 if you have coreutils installed. Other means will work too, of course.")
        group_generic_timeframe.add_argument("-s", "--start", help="Start date [UTC ISO 8601]")
        group_generic_timeframe.add_argument("-e", "--end", nargs="?", default=datetime.datetime.utcnow(), help="End date [UTC ISO 8601] (default: now)")
        parser_create.set_defaults(func=self.create)

        parser_show = subparsers.add_parser("show", help="Display a specific work report", formatter_class=RapportHelpFormatter)
        parser_show.add_argument("-r", "--raw", action="store_true", help="Display the raw report data")
        parser_show.add_argument("report", nargs="?", default=None)
        parser_show.set_defaults(func=self.show)

        parser_edit = subparsers.add_parser("edit", help="Edit parts of a report prior to sending", formatter_class=RapportHelpFormatter)
        parser_edit.add_argument("report", nargs="?", default=None)
        parser_edit.add_argument("-t", "--type", default="email", choices=("email", "html"))
        parser_edit.add_argument("-ep", "--email-part", default="body", choices=("body", "subject"))
        parser_edit.set_defaults(func=self.edit)

        parser_delete = subparsers.add_parser("delete", help="Delete a work report", formatter_class=RapportHelpFormatter)
        parser_delete.add_argument("report", nargs="+", help="The report to delete")
        parser_delete.set_defaults(func=self.delete)

       #parser_email_compose = subparsers.add_parser("email-compose", formatter_class=RapportHelpFormatter)
       #parser_email_compose.set_defaults(func=self.email_compose)
        parser_email_xdg = subparsers.add_parser("email-compose-xdg", help="Use xdg-email to compose, i.e. your preferred mailer under KDE/GNOME/XFCE/etc.", formatter_class=RapportHelpFormatter)
        parser_email_xdg.add_argument("report", nargs="?", default=None)
        parser_email_xdg.set_defaults(func=self.email_xdg)

        parser_help = subparsers.add_parser("help", help="Show this help", formatter_class=RapportHelpFormatter)
        parser_help.set_defaults(func=lambda args: parser.print_help())
       #subparser.add_argument("-h", "--help", action="help",
       #                       help=argparse.SUPPRESS)

        args = parser.parse_args()
        args.func(args)

        #TODO: This is beginning to look ugly. Maybe use oslo.config or sth.:
        if args.verbosity > rapport.config.get_int("rapport", "verbosity"):
            rapport.config.set("rapport", "verbosity", args.verbosity)


def main():
   #try:
        CLI().main()
   #except Exception as e:
   #    print(e, file=sys.stderr)
   #    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
