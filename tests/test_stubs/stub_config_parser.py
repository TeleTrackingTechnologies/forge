# pylint: disable=all
from forge.config.config_handler import ConfigHandler


class StubPluginConfigHandler(ConfigHandler):
    def __init__(self):
        super().__init__('test', 'test_file')

    @staticmethod
    def write_plugin_to_conf(name, url):
        print('stub writing to file')

    @staticmethod
    def get_plugin_entries():
        return [('forge-some-plugin', 'git@bitbucket.org:tele/forge-some-plugin')]

    @staticmethod
    def get_plugins():
        return ['forge-some-plugin']

    @staticmethod
    def get_plugin_install_location():
        return 'path.to.install'
