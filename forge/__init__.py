""" Forge """
#! /usr/bin/env python3
import sys
import os
import configparser
from pathlib import Path
from pluginbase import PluginBase
from tabulate import tabulate


PLUGIN_BASE = PluginBase(package='plugins')


class Application:
    """ Application Class """
    def __init__(self, name):
        self.name = name

        self.registry = {}

        self.plugins = []
        self.parse_conf('/usr/local/etc/forge/', 'conf.ini')
        self.plugins.append('/usr/local/etc/forge/plugins/manage_plugins')
        self.plugin_source = PLUGIN_BASE.make_plugin_source(
            searchpath=self.plugins,
            identifier=self.name)

        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            if callable(getattr(plugin, "register", None)):
                plugin.register(self)

    def register_plugin(self, name, plugin, helptext):
        """A function a plugin can use to register itself."""
        self.registry[name] = (plugin, helptext)

    def print_help(self):
        """ Print Help For All Registered Plugins """
        help_entries = []
        for name in self.registry:
            help_entries.append([name, self.registry[name][1]])
        print(tabulate(help_entries, ['function', 'blurb']))

    def execute(self, command, args):
        """ Execute Plugin """
        if command == 'help':
            self.print_help()
        else:
            self.registry[command][0](args)

    def parse_conf(self, forge_dir, conf_file):
        """ Parse Plugin Configuration File """
        config = configparser.ConfigParser()
        config.read(forge_dir + conf_file)

        if not os.path.exists(forge_dir + conf_file):
            self._init_conf_file(forge_dir + conf_file, config)

        for key in config['plugin-definitions']:
            self.plugins.append(forge_dir + 'plugins/' + key)

    @staticmethod
    def _init_conf_file(path, config):
        config['plugin-definitions'] = {}
        config.write(open(path, 'w'))

def main(args):
    """ Main Function Definition """

    if len(args) > 1:
        Application('forge').execute(args[0], args[1:])
    else:
        Application('forge').execute('help', None)


if __name__ == '__main__':
    main(sys.argv[1:])
