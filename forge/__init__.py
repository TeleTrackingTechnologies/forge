""" Forge """
#! /usr/bin/env python3
import sys
import os
from pathlib import Path
from typing import List, Any
from pluginbase import PluginBase
from tabulate import tabulate
from .config.config_handler import ConfigHandler

CONF_HOME = str(Path(str(Path.home()) + '/.forge'))
CONFIG_FILE_PATH = str(Path(CONF_HOME + '/conf.ini'))
PLUGIN_BASE = PluginBase(package='plugins')
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
INTERNAL_PLUGIN_PATH = str(Path(f'{WORKING_DIR}/_internal_plugins/manage_plugins'))

class Application:
    """ Application Class """
    def __init__(self, name: str, config_handler: ConfigHandler) -> None:
        config_handler.init_conf_dir()
        config_handler.init_conf_file()
        self.name = name
        self.registry = {}

        self.plugins = [
            INTERNAL_PLUGIN_PATH,
            config_handler.get_plugin_install_location()
            ] + config_handler.get_plugins()

        self.plugin_source = PLUGIN_BASE.make_plugin_source(
            searchpath=self.plugins,
            identifier=self.name)
        for plugin_name in self.plugin_source.list_plugins():
            plugin = self.plugin_source.load_plugin(plugin_name)
            if callable(getattr(plugin, "register", None)):
                plugin.register(self)

    def register_plugin(self, name: str, plugin, helptext: str) -> None:
        """A function a plugin can use to register itself."""
        self.registry[name] = (plugin, helptext)

    def print_help(self) -> None:
        """ Print Help For All Registered Plugins """
        help_entries = []
        for name in self.registry:
            help_entries.append([name, self.registry[name][1]])
        print(tabulate(help_entries, ['function', 'blurb']))

    def execute(self, command: str, args: Any) -> None:
        """ Execute Plugin """
        if command == 'help':
            self.print_help()
        else:
            self.registry[command][0](args)

def main(args: list) -> None:
    """ Main Function Definition """
    if len(args) > 1:
        Application(
            'forge',
            ConfigHandler(
                home_dir_path=CONF_HOME,
                file_path_dir=CONFIG_FILE_PATH
            )
        ).execute(args[0], args[1:])
    else:
        Application(
            'forge',
            ConfigHandler(
                home_dir_path=CONF_HOME,
                file_path_dir=CONFIG_FILE_PATH
            )
        ).execute('help', None)


if __name__ == '__main__':
    main(sys.argv[1:])
