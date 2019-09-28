""" Forge """
#! /usr/bin/env python3
import sys
import os
import configparser
from pathlib import Path
from pluginbase import PluginBase
from tabulate import tabulate


PLUGIN_BASE = PluginBase(package='plugins')
CONF_HOME = str(Path(str(Path.home()) + '/.forge'))
CONFIG_FILE_PATH = str(Path(CONF_HOME + '/conf.ini'))
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
INTERNAL_PLUGIN_PATH = str(Path(f'{WORKING_DIR}/_internal_plugins/manage_plugins'))

class Application:
    """ Application Class """
    def __init__(self, name):
        self._init_conf_dir()
        self._init_conf_file()
        self.name = name
        self.registry = {}
        self.plugins = [INTERNAL_PLUGIN_PATH, self._read_plugin_location()]
        self.parse_conf(self._read_plugin_location())
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

    def parse_conf(self, plugin_location):
        """ Parse Plugin Configuration File """
        config = self._get_config_parser()
        for key in config['plugin-definitions']:
            self.plugins.append(str(Path(plugin_location + '/' + key)))

    def _init_conf_file(self):
        config = self._get_config_parser()
        if not os.path.exists(CONFIG_FILE_PATH):
            config['plugin-definitions'] = {}
            config['install-conf'] = {}
            config['install-conf']['pluginlocation'] = str(Path(CONF_HOME + '/plugins')) # this is default plugin install location
            with open(CONFIG_FILE_PATH, 'w') as conf_file:
                config.write(conf_file)

    @staticmethod
    def _init_conf_dir():
        if not os.path.exists(CONF_HOME):
            os.mkdir(CONF_HOME)
    
    def _read_plugin_location(self):
        return self._get_config_parser()['install-conf']['pluginlocation']

    @staticmethod
    def _get_config_parser():
        config_parser = configparser.ConfigParser()
        config_parser.read(CONFIG_FILE_PATH);
        return config_parser
        
def main(args):
    """ Main Function Definition """
    if len(args) > 1:
        Application('forge').execute(args[0], args[1:])
    else:
        Application('forge').execute('help', None)


if __name__ == '__main__':
    main(sys.argv[1:])
