from .manage_plugins_logic.manage_plugins import AddPlugin

def execute(args):
    add_plugin = AddPlugin()
    add_plugin.execute(args)

def helptext():
    return "For managing plugins for use by forge"

def register(app):
    app.register_plugin('manage-plugins', execute, helptext())
