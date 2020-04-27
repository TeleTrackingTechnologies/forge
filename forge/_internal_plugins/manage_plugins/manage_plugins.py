""" Manage Plugins Plugin """
from pathlib import Path
from forge.config.config_handler import ConfigHandler
from .manage_plugins_logic.manage_plugins import ManagePlugins
from .manage_plugins_logic.plugin_puller import PluginPuller
CONF_HOME = str(Path(str(Path.home()) + '/.forge'))
CONFIG_FILE_PATH = str(Path(CONF_HOME + '/conf.ini'))

def execute(args: list) -> None:
    """ Plugin Execution Definition """
    config_handler = ConfigHandler(
        home_dir_path=CONF_HOME,
        file_path_dir=CONFIG_FILE_PATH
    )
    manage_plugins_logic = ManagePlugins(PluginPuller(config_handler), config_handler)
    manage_plugins_logic.execute(args)


def helptext() -> str:
    """ Simple Helptext For Plugin """
    return "For managing plugins for use by forge."


def register(app) -> None:
    """ Plugin Registration """
    app.register_plugin('manage-plugins', execute, helptext())
