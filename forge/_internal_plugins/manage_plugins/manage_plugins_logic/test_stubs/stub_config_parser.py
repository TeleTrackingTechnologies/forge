# pylint: disable=all
from .....config.config_handler import ConfigHandler
class StubPluginConfigHandler(ConfigHandler):
    @staticmethod
    def write_plugin_to_conf(name, url):
        print('stub writing to file')

    @staticmethod
    def get_plugin_entries():
        return [('some_name', 'some_url')]
