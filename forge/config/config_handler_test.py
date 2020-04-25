# pylint: disable=all
import unittest
import configparser
import os
from pathlib import Path
from .config_handler import ConfigHandler

CONF_HOME = str(Path(str('tmp') + '/.forge'))
CONFIG_FILE_PATH = str(Path('tmp' + '/conf.ini'))

class ConfigHandlerTest(unittest.TestCase):
    
    def test_write_plugin_to_conf(self):
        name = 'somepluginname'
        url = 'url.for.plugin.git'
        unit_under_test = ConfigHandler(home_dir_path=CONF_HOME, file_path_dir=CONFIG_FILE_PATH)
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
        unit_under_test = ConfigHandler(home_dir_path=CONF_HOME, file_path_dir=CONFIG_FILE_PATH)
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
        conf_handler = ConfigHandler(
                home_dir_path=CONF_HOME,
                file_path_dir=CONFIG_FILE_PATH
            )
        conf_handler.init_conf_dir()
        conf_handler.init_conf_file()
            