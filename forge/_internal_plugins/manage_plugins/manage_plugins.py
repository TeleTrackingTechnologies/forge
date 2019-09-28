""" Manage Plugins Plugin """
from forge.config.config_handler import ConfigHandler
from .manage_plugins_logic.manage_plugins import ManagePlugins
from .manage_plugins_logic.plugin_puller import PluginPuller

def execute(args):
    """ Plugin Execution Definition """
    config_handler = ConfigHandler()
    manage_plugins_logic = ManagePlugins(PluginPuller(config_handler), config_handler)
    manage_plugins_logic.execute(args)


def helptext():
    """ Simple Helptext For Plugin """
    return "For managing plugins for use by forge."


def register(app):
    """ Plugin Registration """
    app.register_plugin('manage-plugins', execute, helptext())
