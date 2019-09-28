# pylint: disable=all
import unittest
import configparser
import os

from .config_handler import ConfigHandler
from .config_handler import CONFIG_FILE_PATH
class ConfigHandlerTest(unittest.TestCase):
    
    def test_write_plugin_to_conf(self):
        name = 'somepluginname'
        url = 'url.for.plugin.git'
        unit_under_test = ConfigHandler()
        unit_under_test.write_plugin_to_conf(name, url)

        parser = configparser.ConfigParser()
        parser.sections()
        parser.read(CONFIG_FILE_PATH)
        plugin_entries = dict(parser.items('plugin-definitions'))

        try:
            self.assertIsNotNone(plugin_entries[name])
            self.assertEqual(plugin_entries[name], url)
        except KeyError:
            self.fail()

    def test_read_plugin_entries(self):
        unit_under_test = ConfigHandler()
        unit_under_test.write_plugin_to_conf('some_name', 'someurl')
        unit_under_test.write_plugin_to_conf('someothername', 'someotherurl')

        entries = unit_under_test.get_plugin_entries()

        self.assertIsNotNone(entries)       
        entries_as_dict = dict(entries)

        try:
            self.assertEquals(entries_as_dict['some_name'], 'someurl')
            self.assertEquals(entries_as_dict['someothername'], 'someotherurl')
        except KeyError:
            self.fail()
       
    def tearDown(self):
        super().tearDown()
        os.remove(CONFIG_FILE_PATH)

    def setUp(self):
        super().setUp()   
        ConfigHandler().init_conf_file()
            