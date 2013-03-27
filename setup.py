#!/usr/bin/env python

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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import rapport
from rapport.setup import get_cmdclass, parse_requirements


install_requires = parse_requirements("tools/install-requires.txt")
tests_requires = parse_requirements("tools/test-requires.txt")

setup(
    name="rapport",
    version=rapport.__version__,
    license="GPLv2",
    description=rapport.__doc__,
    long_description=open("README.rst").read(),
    author=rapport.__author__.rsplit(" ", 1)[0],
    author_email=rapport.__author__.rsplit(" ", 1)[1][1:-1],
    url="http://github.com/saschpe/rapport",
    scripts=["scripts/rapport"],
    packages=["rapport", "rapport.plugins"],
    #package_data={"rapport": ["templates/*"]},
    setup_requires=install_requires + tests_requires,
    install_requires=install_requires,
    cmdclass=get_cmdclass(),
    tests_require=tests_requires,
    test_suite="nose.collector",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
    ],
)
