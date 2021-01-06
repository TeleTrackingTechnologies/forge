""" Forge """

import os
from json import loads
from pathlib import Path
from typing import Dict, List, Any

from tabulate import tabulate
from halo import Halo

from .exceptions import PluginManagementFatalException

FORGE_PATH = os.path.join(Path.home(), '.forge')
PLUGIN_PATH = os.path.join(FORGE_PATH, 'venvs')


def get_plugin_paths() -> List[str]:
    """ Fet paths of installed plugins """
    paths = []
    for venv in os.listdir(PLUGIN_PATH):
        paths.append(os.path.join(PLUGIN_PATH, venv))
    return paths


def get_forge_plugin_command_names() -> List[str]:
    """ Returns a list of plugin command names"""
    return [
        get_command_from_config(plugin_config)
        for plugin_config in get_plugins()
    ]


def get_pipx_config(plugin_path: str) -> Dict[Any, Any]:
    """ Return config data from pipx venv metadata file """
    config_file_path = os.path.join(plugin_path, 'pipx_metadata.json')
    try:
        with open(config_file_path) as config_file:
            raw_data = config_file.read()
            if raw_data:
                return loads(raw_data)
            raise PluginManagementFatalException()

    except:
        raise PluginManagementFatalException(
            f'Problem reading json file expected at {plugin_path}'
        ) from None


def filter_forge_plugins(plugin_configs: List[Dict]) -> List[Dict]:
    """ Filters out non-forge plugins """
    filtered_plugins = []
    for config in plugin_configs:
        if config and config['main_package']['package'].startswith('forge-'):
            filtered_plugins.append(config)
    return filtered_plugins


def get_command_from_config(plugin_config: Dict) -> str:
    """ Gets the plugin command from its config """
    return str(plugin_config['main_package']['apps'][0].replace('.exe', ''))


def get_plugins() -> List[Dict]:
    """ Get installed forge plugins """
    plugin_configs = []
    for plugin_path in get_plugin_paths():
        plugin_configs.append(get_pipx_config(plugin_path))

    return filter_forge_plugins(plugin_configs=plugin_configs)


def list_plugins() -> None:
    """ List installed forge plugins """
    tabulated_data = [
        (get_command_from_config(config), config['main_package']['package_version'])
        for config in get_plugins()]

    if len(tabulated_data) == 0:
        Halo().warn('No forge plugins installed yet! - Run forge --help for help')
    else:
        print(tabulate(tabulated_data, ['plugin', 'version']), end='\n\n')
