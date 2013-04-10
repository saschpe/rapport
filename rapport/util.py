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

"""Various utility functions.
"""

import datetime
import re
import subprocess

_FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
_ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')


def camelcase_to_underscores(word):
    """Converts a CamelCase word into an under_score word.

        >>> camelcase_to_underscores("CamelCaseCase")
        'camel_case_case'
        >>> camelcase_to_underscores("getHTTPResponseCode")
        'get_http_response_code'
    """
    s1 = _FIRST_CAP_RE.sub(r'\1_\2', word)
    return _ALL_CAP_RE.sub(r'\1_\2', s1).lower()


def silent_popen(args, **kwargs):
    """Wrapper for subprocess.Popen with suppressed output.

    STERR is redirected to STDOUT which is piped back to the
    calling process and returned as the result.
    """
    return subprocess.Popen(args,
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE, **kwargs).communicate()[0]


def datetime_from_iso8601(string):
    """Small helper that parses ISO-8601 date strings.
    """
    if string.endswith("Z"):
        string = string[:-1]  # Date string is UTC
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%f")
