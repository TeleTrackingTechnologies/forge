class StubPluginConfigHandler:
    @staticmethod
    def write_plugin_to_conf(name, url):
        """ Write Plugin Info to Config File """
        print('stub writing to file')

    @staticmethod
    def read_plugin_entries():
        """Reads installed plugin entries"""
        return [('some_name', 'some_url')]
