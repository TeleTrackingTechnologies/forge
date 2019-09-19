# pylint: disable=all
class StubPluginConfigHandler:
    @staticmethod
    def write_plugin_to_conf(name, url):
        print('stub writing to file')

    @staticmethod
    def read_plugin_entries():
        return [('some_name', 'some_url')]
