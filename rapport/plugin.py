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

import os
import sys
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from rapport.config import USER_CONFIG_DIR
import rapport.config
import rapport.util


class Plugin(object):
    def __init__(self, alias=None, url=None, login=None, password=None):
        self.alias = alias
        self.url = url
        self.login = login
        self.password = password

        if alias == "":
            self.alias == self.__str__()

        if url and type(url) is not urlparse.ParseResult:
            self.url = urlparse.urlparse(url)

    def _results(self, dict={}):
        """Helper to merge a dict with cross-plugin defaults.

        All plugin sub-classes share some config values, i.e.  alias, url,
        login and password. This help should be used in the :collect: method
        of any Plugin implementation.

           >>> import rapport.plugin
           >>> c = rapport.plugin.Plugin(alias="a", url="http://example.com", login="u")
           >>> c._results()
           {'url': ParseResult(scheme='http', netloc='example.com', path='', params='', query='', fragment=''), 'alias': 'a', 'login': 'u', 'plugin': 'plugin'}
           >>> c._results({'mykey': 'mykey'})
           {'url': ParseResult(scheme='http', netloc='example.com', path='', params='', query='', fragment=''), 'alias': 'a', 'login': 'u', 'mykey': 'mykey', 'plugin': 'plugin'}
        """
        results = {"plugin": str(self),
                   "alias": self.alias,
                   "url": self.url,
                   "login": self.login}
        results.update(dict)
        return results

    def __str__(self):
        """Returns the class name in underscores.

        Additionally, for sub-classes, the suffix '_plugin' is split off.

            >>> import rapport.plugin
            >>> c = rapport.plugin.Plugin()
            >>> str(c)
            'plugin'
        """
        return rapport.util.camelcase_to_underscores(self.__class__.__name__).rsplit("_plugin")[0]

    def collect(self, timeframe):
        raise NotImplementedError()


def _get_plugin_dirs():
    """Return a list of directories where plugins may be located.
    """
    plugin_dirs = [
        os.path.expanduser(os.path.join(USER_CONFIG_DIR, "plugins")),
        os.path.join("rapport", "plugins")  # Local dev tree
    ]
    return plugin_dirs


def _path_to_module(path):
    """Translates paths to *.py? files into module paths.

        >>> _path_to_module("rapport/bar.py")
        'rapport.bar'
        >>> _path_to_module("/usr/lib/rapport/bar.py")
        'rapport.bar'
    """
    # Split of preceeding path elements:
    path = "rapport" + path.split("rapport")[1]
    # Split of ending and replace os.sep with dots:
    path = path.replace(os.sep, ".").rsplit(".", 1)[0]
    return path


def discover():
    """Find and load all available plugins.
    """
    plugin_files = []

    for plugin_dir in _get_plugin_dirs():
        if os.path.isdir(plugin_dir):
            for plugin_file in os.listdir(plugin_dir):
                if plugin_file.endswith(".py") and not plugin_file == "__init__.py":
                    plugin_files.append(os.path.join(plugin_dir, plugin_file))

    if rapport.config.get_int("rapport", "verbosity") >= 2:
        print("Found plugin modules: {0}".format(plugin_files))

    for plugin_file in plugin_files:
        if rapport.config.get_int("rapport", "verbosity") >= 2:
            print("Importing module {0}".format(_path_to_module(plugin_file)))
        __import__(_path_to_module(plugin_file))


_PLUGIN_CATALOG = {}


def register(name, klass):
    """Add a plugin to the plugin catalog.
    """
    if rapport.config.get_int("rapport", "verbosity") >= 1:
        print("Registered plugin: {0}".format(name))
    _PLUGIN_CATALOG[name] = klass


def init(name, *args, **kwargs):
    """Instantiate a plugin from the catalog.
    """
    if name in _PLUGIN_CATALOG:
        if rapport.config.get_int("rapport", "verbosity") >= 2:
            print("Initialize plugin {0}: {1} {2}".format(name, args, kwargs))
        try:
            return _PLUGIN_CATALOG[name](*args, **kwargs)
        except (ValueError, TypeError) as e:
            print("Failed to initialize plugin {0}: {1}!".format(name, e), file=sys.stderr)
    else:
        print("Failed to initialize plugin {0}: Not in catalog!".format(name), file=sys.stderr)


def init_from_config():
    plugins = []
    for plugin in rapport.config.plugins():
        plugins.append(init(**plugin))
    return list(filter(bool, plugins))


def catalog():
    """Returns the list of registered plugins.
    """
    return _PLUGIN_CATALOG.keys()
