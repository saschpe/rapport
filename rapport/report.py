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

import datetime
import os
import shutil
import sys
if sys.version_info > (3, 3):
    import concurrent.futures as futures
else:
    import futures

import rapport.config
import rapport.template
import rapport.util


def _get_reports_path(report=None):
    path_parts = ["~", ".rapport", "reports"]
    if report:
        path_parts.append(report)
    return os.path.expanduser(os.path.join(*path_parts))


def list_reports():
    """Returns a list of created reports.
    """
    return sorted(os.listdir(_get_reports_path()))


def get_report(report=None):
    """Returns details of a specific report
    """
    if not report:
        report = list_reports()[-1:][0]
    report_path = _get_reports_path(report)
    report_dict = {"report": report}
    for filename in os.listdir(report_path):
        with open(os.path.join(report_path, filename), "r") as f:
            report_dict[filename] = f.read()
    return report_dict


def create_report(plugins, timeframe):
    report_date_string = timeframe.end.strftime(rapport.util.ISO8610_FORMAT)
    report_path = _get_reports_path(report_date_string)
    if not os.path.exists(report_path):
        os.makedirs(report_path)

    # Execute all plugins in parallel and join on results:
    results = {}
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        plugin_futures = dict((executor.submit(p.collect, timeframe), p) for p in plugins)
        for future in futures.as_completed(plugin_futures):
            plugin = plugin_futures[future]
            try:
                if rapport.config.get_int("rapport", "verbosity") >= 2:
                    print "Result for {0}: {1}".format(plugin.alias, future.result())
                tmpl = rapport.template.get_template(plugin, "text")
                if tmpl:
                    results[plugin] = tmpl.render(future.result())
            except Exception as e:
                print >>sys.stderr, "Failed plugin {0}:{1}: {2}!".format(plugin, plugin.alias, e)

    results_dict = {"login": rapport.config.get("user", "login"),
                    "date": report_date_string,
                    "plugins": plugins,
                    "results": results}

    # Render mail body template:
    template_email_body = rapport.template.get_template("body", type="email")
    email_body = template_email_body.render(results_dict)
    email_body_file = os.path.join(report_path, "email.body.text")
    with open(email_body_file, "w") as report:
        report.write(email_body)

    # We can re-use the e-mail body as the general report body:
    results_dict["body"] = email_body

    # Render mail subject template:
    template_email_subject = rapport.template.get_template("subject", type="email")
    email_subject = template_email_subject.render(results_dict)
    email_subject_file = os.path.join(report_path, "email.subject.text")
    with open(email_subject_file, "w") as report:
        report.write(email_subject)

    #TODO: Maybe even create a Result class and return that instead of a dict?
    return results_dict


def delete_report(report):
    report_path = _get_reports_path(report)
    shutil.rmtree(report_path)
