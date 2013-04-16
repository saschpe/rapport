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

import rapport.config
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


def create_report(date=datetime.datetime.now()):
    report_path = _get_reports_path(date.strftime(rapport.util.ISO8610_FORMAT))
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    return report_path


def delete_report(report):
    report_path = _get_reports_path(report)
    shutil.rmtree(report_path)
