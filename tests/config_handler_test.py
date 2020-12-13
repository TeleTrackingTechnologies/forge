import configparser
import os
import pytest

from pathlib import Path
from shutil import rmtree


from forge.config.config_handler import ConfigHandler

CONF_HOME = str(Path(str('tmp') + '/.forge'))
CONFIG_FILE_PATH = str(Path('tmp' + '/conf.ini'))


@pytest.fixture(autouse=True)
def setup_and_teardown():
    conf_handler = ConfigHandler(
        home_dir_path=CONF_HOME,
        file_path_dir=CONFIG_FILE_PATH
    )
    conf_handler.init_conf_dir()
    conf_handler.init_conf_file()
    yield
    os.remove(CONFIG_FILE_PATH)
    rmtree('tmp', ignore_errors=True)


def test_write_plugin_to_conf():
    name = 'somepluginname'
    url = 'url.for.plugin.git'
    config_handler = ConfigHandler(home_dir_path=CONF_HOME, file_path_dir=CONFIG_FILE_PATH)
    config_handler.write_plugin_to_conf(name, url)

    parser = configparser.ConfigParser()
    parser.sections()
    parser.read(CONFIG_FILE_PATH)
    plugin_entries = dict(parser.items('plugin-definitions'))

    assert plugin_entries[name] is not None
    assert plugin_entries[name] == url


def test_read_plugin_entries():
    config_handler = ConfigHandler(home_dir_path=CONF_HOME, file_path_dir=CONFIG_FILE_PATH)
    config_handler.write_plugin_to_conf('some_name', 'someurl')
    config_handler.write_plugin_to_conf('someothername', 'someotherurl')

    entries = config_handler.get_plugin_entries()

    assert entries is not None
    entries_as_dict = dict(entries)

    assert entries_as_dict['some_name'] == 'someurl'
    assert entries_as_dict['someothername'] == 'someotherurl'


def test_get_plugins():
    config_handler = ConfigHandler(home_dir_path=CONF_HOME, file_path_dir=CONFIG_FILE_PATH)
    config_handler.write_plugin_to_conf('some_name', 'someurl')
    config_handler.write_plugin_to_conf('someothername', 'someotherurl')

    plugins = config_handler.get_plugins()

    plugin_1 = os.path.join('tmp', '.forge', 'plugins', 'some_name')
    plugin_2 = os.path.join('tmp', '.forge', 'plugins', 'someothername')

    assert plugins == [plugin_1, plugin_2]


def test_get_plugin_install_location():
    config_handler = ConfigHandler(home_dir_path=CONF_HOME, file_path_dir=CONFIG_FILE_PATH)

    assert config_handler.get_plugin_install_location() == os.path.join('tmp', '.forge', 'plugins')
