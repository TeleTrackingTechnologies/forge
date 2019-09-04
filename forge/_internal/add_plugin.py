from .add_plugin_logic.add_plugin_logic import AddPlugin

def execute(args):
    add_plugin = AddPlugin()
    add_plugin.execute(args)

def helptext():
    return "For adding plugins to forge application."

def register(app):
    app.register_plugin('add-plugin', execute, helptext())
