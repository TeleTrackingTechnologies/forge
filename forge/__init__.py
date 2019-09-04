#! /usr/bin/env python3

import sys
import configparser
from pluginbase import PluginBase
from pathlib import Path
from tabulate import tabulate

plugin_base = PluginBase(package='plugins')


class Application(object):

    def __init__(self, name):
        self.name = name

        self.registry = {}

        plugins = self.parse_conf('/usr/local/etc/forge/', 'conf.ini')
        plugins.append('/usr/local/etc/forge/plugins/add_plugin')
        print(plugins)
        self.plugin_source = plugin_base.make_plugin_source(
            searchpath=plugins,
            identifier=self.name)

        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            if callable(getattr(plugin, "register", None)):
                plugin.register(self)

    def register_plugin(self, name, plugin, helptext):
        """A function a plugin can use to register itself."""
        self.registry[name] = (plugin, helptext)

    def print_help(self):
        help_entries = []
        for name in self.registry:
            help_entries.append([name, self.registry[name][1]])
        print(tabulate(help_entries, ['function', 'blurb']))

    def execute(self, command, args):
        if command == 'help':
            self.print_help()
        else:
            self.registry[command][0](args)

    def parse_conf(self, forge_dir, conf_file):
        try:
            config = configparser.ConfigParser()
            config.read(forge_dir + conf_file)
            plugins_list = []
            for key in config['plugin-definitions']:
                plugins_list.append(forge_dir + 'plugins/' + key)
            return plugins_list
        except:
            # TODO: improve error handling
            print('config parse failed')



def main(args):
    print("Forge\n")
    if len(args) > 1:
        Application('forge').execute(args[0], args[1:])
    else:
        Application('forge').execute('help', None)


if __name__ == '__main__':
    main(sys.argv[1:])
