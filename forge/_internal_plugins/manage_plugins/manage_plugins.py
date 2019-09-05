""" Manage Plugins Plugin """
from .manage_plugins_logic.manage_plugins import AddPlugin

def execute(args):
    """ Plugin Execution Definition """
    add_plugin = AddPlugin()
    add_plugin.execute(args)

def helptext():
    """ Simple Helptext For Plugin """
    return "For managing plugins for use by forge"

def register(app):
    """ Plugin Registration """
    app.register_plugin('manage-plugins', execute, helptext())
