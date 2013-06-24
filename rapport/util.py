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

"""Various utility functions.
"""

import datetime
import re
import site
import sys
import subprocess


_FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
_ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')

ISO8610_FORMAT = "%Y-%m-%dT%H:%M:%S"
ISO8610_FORMAT_MICROSECONDS = "%Y-%m-%dT%H:%M:%S.%f"


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


def datetime_from_iso8601(date):
    """Small helper that parses ISO-8601 date dates.

        >>> datetime_from_iso8601("2013-04-10T12:52:39")
        datetime.datetime(2013, 4, 10, 12, 52, 39)
        >>> datetime_from_iso8601("2013-01-07T12:55:19.257")
        datetime.datetime(2013, 1, 7, 12, 55, 19, 257000)
    """
    format = ISO8610_FORMAT
    if date.endswith("Z"):
        date = date[:-1]  # Date date is UTC
    if re.match(".*\.\d+", date):
        # Date includes microseconds
        format = ISO8610_FORMAT_MICROSECONDS
    return datetime.datetime.strptime(date, format)


def under_virtualenv():
    return hasattr(sys, "real_prefix")


def getsitepackages():
    if hasattr(site, "getsitepackages"):
        return site.getsitepackages()
    else:
        # Workaround for older Python versions and some broken virtualenvs:
        if under_virtualenv():
            return []
        else:
            from distutils.sysconfig import get_python_lib
            return [get_python_lib(True)]
