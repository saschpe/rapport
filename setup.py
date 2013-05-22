#!/usr/bin/env python

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
    license="Apache-2.0",
    description="Work report generator for the lazy",
    long_description=open("README.rst").read(),
    author=rapport.__author__.rsplit(" ", 1)[0],
    author_email=rapport.__author__.rsplit(" ", 1)[1][1:-1],
    url="http://github.com/saschpe/rapport",
    scripts=["scripts/rapport"],
    packages=["rapport", "rapport.plugins"],
    package_data={"rapport": ["templates/email/*",
                              "templates/plugin/*",
                              "templates/web/*",
                              "config/*"],
                  "": ["LICENSE"]},
    setup_requires=install_requires + tests_requires,
    install_requires=install_requires,
    cmdclass=get_cmdclass(),
    tests_require=tests_requires,
    test_suite="nose.collector",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
