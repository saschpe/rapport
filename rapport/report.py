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

from __future__ import print_function

import glob
import os
import shutil
import subprocess
import sys
if sys.version_info > (3, 3):
    import concurrent.futures as futures
else:
    import futures
import traceback

import jinja2

XDG_CONFIG_DATA_DIR = os.getenv('XDG_DATA_HOME') or \
                      os.path.expanduser(os.path.join("~", ".local", "share"))
USER_DATA_DIR       = os.path.join(XDG_CONFIG_DATA_DIR, "rapport")

from rapport.config import USER_CONFIG_DIR
import rapport.template
import rapport.util


def _get_reports_path(report=None):
    path_parts = [USER_DATA_DIR, "reports"]
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


def edit_report(report=None, type="email", email_part="body"):
    if not report:
        report = list_reports()[-1:][0]
    report_path = _get_reports_path(report)
    editor = os.getenv("EDITOR", "vi")
    if type == "email":
        report_file = "{0}.{1}.text".format(type, email_part)
    elif type == "html":
        report_file = "index.html"
    subprocess.call([editor, os.path.join(report_path, report_file)])


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
                    print("Result for {0}: {1}".format(plugin.alias, future.result()))
                tmpl = rapport.template.get_template(plugin, "text")
                if tmpl:
                    results[plugin] = tmpl.render(future.result())
            except jinja2.TemplateSyntaxError as e:
                print >>sys.stderr, "Syntax error in plugin {0} at {1} line {2}: {3}".format(plugin, e.name, e.lineno, e.message)
            except Exception as e:
                print("Failed plugin {0}:{1}: {2}!".format(plugin, plugin.alias, e), file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)

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
    """Delete report(s), supports globbing.
    """
    for path in glob.glob(os.path.join(_get_reports_path(), report)):
        shutil.rmtree(path)
