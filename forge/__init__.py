""" Forge """
#! /usr/bin/env python3
import os
import sys
from inspect import getmembers, isfunction
from pathlib import Path
from pprint import pprint
from typing import Any, List

import pluginbase
from tabulate import tabulate

from .config.config_handler import ConfigHandler

CONF_HOME = str(Path(str(Path.home()) + '/.forge'))
CONFIG_FILE_PATH = str(Path(CONF_HOME + '/conf.ini'))
PLUGIN_BASE = pluginbase.PluginBase(package='forge.plugins')
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
            INTERNAL_PLUGIN_PATH
        ] + config_handler.get_plugins()

        self.plugin_source = PLUGIN_BASE.make_plugin_source(
            searchpath=self.plugins,
            identifier=self.name)

        for plugin_name in self.plugin_source.list_plugins():
            if plugin_name.endswith('_logic'):
                continue

            plugin = self.plugin_source.load_plugin(plugin_name)

            plugin.register(self)

    def register_plugin(self, name: str, plugin, helptext: str) -> None:
        """A function a plugin can use to register itself."""
        self.registry[name] = (plugin, helptext)

    def print_help(self) -> None:
        """ Print Help For All Registered Plugins """
        print('\nTo use forge plugins try running a plugin like this:', end='\n\n')
        print('\tforge manage-plugins -h', end='\n\n')

        help_entries = []
        for name in self.registry:
            help_entries.append([name, self.registry[name][1]])
        print(tabulate(help_entries, ['plugin', 'description']), end='\n\n')

    def execute(self, command: str, args: Any) -> None:
        """ Execute Plugin """
        if command == 'help':
            self.print_help()
        else:
            if command not in self.registry:
                print(f'Unknown command: {command}')
                sys.exit(1)
            else:
                self.registry[command][0](args)


def main(args: list) -> None:
    """ Main Function Definition """
    name = 'forge'
    config_handler = ConfigHandler(
        home_dir_path=CONF_HOME,
        file_path_dir=CONFIG_FILE_PATH
    )
    app = Application(
        name=name,
        config_handler=config_handler
    )

    if len(args) > 0:
        app.execute(args[0], args[1:])
    else:
        app.execute('help', None)


if __name__ == '__main__':
    main(args=sys.argv[1:])
