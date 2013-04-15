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
E-Mail functionality.
"""

import subprocess

import rapport.config


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
