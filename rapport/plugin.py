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

import os
import site
import sys
import traceback
import urlparse

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
           {'url': 'http://example.com', 'alias': 'a', 'login': 'u'}
           >>> c._results({'mykey': 'mykey'})
           {'url': 'http://example.com', 'alias': 'a', 'login': 'u', 'mykey': 'mykey'}
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
        os.path.expanduser(os.path.join("~", ".rapport", "plugins")),
        os.path.join("rapport", "plugins")  # Local dev tree
    ]  + map(lambda d: os.path.join(d, "rapport", "plugins"), site.getsitepackages())
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
        print "Found plugin modules: {0}".format(plugin_files)
    for plugin_file in plugin_files:
        if rapport.config.get_int("rapport", "verbosity") >= 2:
            print "Importing module {0}".format(_path_to_module(plugin_file))
        __import__(_path_to_module(plugin_file))


_PLUGIN_CATALOG = {}


def register(name, klass):
    """Add a plugin to the plugin catalog.
    """
    if rapport.config.get_int("rapport", "verbosity") >= 1:
        print "Registered plugin: {0}".format(name)
    _PLUGIN_CATALOG[name] = klass


def init(name, *args, **kwargs):
    """Instantiate a plugin from the catalog.
    """
    if name in _PLUGIN_CATALOG:
        if rapport.config.get_int("rapport", "verbosity") >= 2:
            print "Initialize plugin {0}: {1} {2}".format(name, args, kwargs)
        try:
            return _PLUGIN_CATALOG[name](*args, **kwargs)
        except (ValueError, TypeError) as e:
            print >>sys.stderr, "Failed to initialize plugin {0}: {1}!".format(name, e)
    else:
        print >>sys.stderr, "Failed to initialize plugin {0}: Not in catalog!".format(name)


def init_from_config():
    plugins = []
    for plugin in rapport.config.plugins():
        plugins.append(init(**plugin))
    return filter(bool, plugins)


def catalog():
    """Returns the list of registered plugins.
    """
    return _PLUGIN_CATALOG.keys()
