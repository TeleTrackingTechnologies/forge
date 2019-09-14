# pylint: disable=all
import unittest
import configparser
import os
from forge._internal_plugins.manage_plugins.manage_plugins_logic.plugin_config_handler import PluginConfigHandler

class PluginConfigHandlerTest(unittest.TestCase):
    
    def test_write_plugin_to_conf(self):
        name = 'somepluginname'
        url = 'url.for.plugin.git'
        unit_under_test = PluginConfigHandler()
        unit_under_test.write_plugin_to_conf(name, url)

        parser = configparser.ConfigParser()
        parser.sections()
        parser.read(unit_under_test.CONF_FILE_LOCATION)
        plugin_entries = dict(parser.items('plugin-definitions'))

        try:
            self.assertIsNotNone(plugin_entries[name])
            self.assertEqual(plugin_entries[name], url)
        except KeyError:
            self.fail()

    def test_read_plugin_entries(self):
        unit_under_test = PluginConfigHandler()
        unit_under_test.write_plugin_to_conf('some_name', 'someurl')
        unit_under_test.write_plugin_to_conf('someothername', 'someotherurl')

        entries = unit_under_test.read_plugin_entries()

        self.assertIsNotNone(entries)       
        entries_as_dict = dict(entries)

        try:
            self.assertEquals(entries_as_dict['some_name'], 'someurl')
            self.assertEquals(entries_as_dict['someothername'], 'someotherurl')
        except KeyError:
            self.fail()
       
    def tearDown(self):
        super().tearDown()
        os.remove(PluginConfigHandler.CONF_FILE_LOCATION)

    def setUp(self):
        super().setUp()   

        if not os.path.exists(PluginConfigHandler.CONF_FILE_LOCATION):
            config = configparser.ConfigParser()
            config.read(PluginConfigHandler.CONF_FILE_LOCATION)
            config['plugin-definitions'] = {}
            with open(PluginConfigHandler.CONF_FILE_LOCATION, 'w') as f:
                config.write(f)
