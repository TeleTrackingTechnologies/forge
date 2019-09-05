""" Manage Plugins Plugin """
from .manage_plugins_logic.manage_plugins import ManagePlugins
from .manage_plugins_logic.plugin_puller import PluginPuller
from .manage_plugins_logic.plugin_config_handler import PluginConfigHandler

def execute(args):
    """ Plugin Execution Definition """
    manage_plugins_logic = ManagePlugins(PluginPuller(), PluginConfigHandler())
    manage_plugins_logic.execute(args)


def helptext():
    """ Simple Helptext For Plugin """
    return "For managing plugins for use by forge"


def register(app):
    """ Plugin Registration """
    app.register_plugin('manage-plugins', execute, helptext())
