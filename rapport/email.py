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
E-Mail functionality.
"""

import subprocess


def compose():
    raise NotImplementedError()


def send():
    raise NotImplementedError()


def xdg_compose(to, subject, body=None, cc=None, bcc=None):
    """Use xdg-email to compose in an X environment.

    Needs xdg-utils and a running X session. Works with GNOME, KDE,
    MATE, XFCE, ...
    """
    command = ["xdg-email", "--utf8", "--subject", subject]

    if body:
        command += ["--body", body]
    if cc:
        if type(cc) is list:
            cc = ", ".join(cc)
        command += ["--cc", cc]
    if bcc:
        if type(bcc) is list:
            bcc = ", ".join(bcc)
        command += ["--bcc", bcc]
    if type(to) is list:
        to = ", ".join(to)
    command.append(to)
    return subprocess.call(command)
