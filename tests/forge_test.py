import os

import pytest
from forge import forge
from forge.exceptions import (PluginManagementFatalException,
                              PluginManagementWarnException)
from mock import call, mock_open, patch

from .conftest import multi_mock_open


@patch('os.listdir', return_value=['plugin1', 'plugin2'])
def test_get_plugin_paths(mocked_listdir):

    forge.PLUGIN_PATH = os.path.join('home', 'user', '.forge', 'venvs')

    expected_paths = [
        'home|user|.forge|venvs|plugin1',
        'home|user|.forge|venvs|plugin2'
    ]

    plugin_paths = forge.get_plugin_paths()

    normalized_plugin_paths = [path.replace(os.path.sep, '|') for path in plugin_paths]

    assert normalized_plugin_paths == expected_paths


def test_get_pipx_config():

    fake_config_json = '{"a":"something", "b":"another"}'

    with patch("builtins.open", mock_open(read_data=fake_config_json)):
        config_data = forge.get_pipx_config('some_path')

    assert config_data == {'a': 'something', 'b': 'another'}


def test_get_pipx_config_bad_json_data():
    fake_config_json = '{"a":no quote heres, or here:"another"}'

    with pytest.raises(forge.PluginManagementFatalException) as err:
        with patch("builtins.open", mock_open(read_data=fake_config_json)):
            forge.get_pipx_config('some_path')

    assert str(err.value) == 'Problem reading json file expected at some_path'


def test_get_pipx_config_no_data():
    with pytest.raises(forge.PluginManagementFatalException) as err:
        with patch("builtins.open", mock_open(read_data='')):
            forge.get_pipx_config('some_path')

    assert str(err.value) == 'Problem reading json file expected at some_path'


def test_filer_forge_plugins():
    mock_config_list = [
        {'main_package': {
            'package': 'package1'
        }},
        {'main_package': {
            'package': 'forge-package2'
        }},
        {},
        {'main_package': {
            'package': 'forge-package4'
        }},
    ]

    expected_configs = [mock_config_list[1], mock_config_list[3]]

    assert forge.filter_forge_plugins(plugin_configs=mock_config_list) == expected_configs


def test_get_command_from_config():

    mock_plugin_config = {
        'main_package': {
            'apps': [
                'plugin-name.exe'
            ]
        }}

    assert forge.get_command_from_config(mock_plugin_config) == 'plugin-name'


@patch('os.listdir', return_value=['forge-plugin1', 'forge-plugin2', 'non_plugin'])
def test_get_plugins(mocked_listdir):
    forge.PLUGIN_PATH = os.path.join('home', 'user', '.forge', 'venvs')

    fake_config_jsons = [
        '{"main_package": {"package": "forge-plugin1"}}',
        '{"main_package": {"package": "forge-plugin2"}}',
        '{"main_package": {"package": "non_plugin"}}'
    ]

    with patch("builtins.open", multi_mock_open(*fake_config_jsons)):
        filtered_plugin_configs = forge.get_plugins()

    expected_plugin_configs = [
        {'main_package': {'package': 'forge-plugin1'}},
        {'main_package': {'package': 'forge-plugin2'}}
    ]

    assert filtered_plugin_configs == expected_plugin_configs


@patch('forge.forge.Halo')
@patch('forge.forge.tabulate')
@patch('os.listdir', return_value=['forge-plugin1', 'forge-plugin2', 'non_plugin'])
def test_list_plugins(mocked_listdir, mocked_tabulate, mocked_spinner):
    forge.PLUGIN_PATH = os.path.join('home', 'user', '.forge', 'venvs')

    fake_config_jsons = [
        '{"main_package": {"package": "forge-plugin1", "apps": ["plugin1.exe"], "package_version":"1.0.0"}}',
        '{"main_package": {"package": "forge-plugin2", "apps": ["plugin2"], "package_version":"0.0.1"}}',
        '{"main_package": {"package": "non_plugin", "apps": ["non_plugin.exe"], "package_version":"0.0.2"}}'
    ]

    with patch("builtins.open", multi_mock_open(*fake_config_jsons)):
        forge.list_plugins()

    mocked_tabulate.assert_called_once_with(
        [('plugin1', '1.0.0'), ('plugin2', '0.0.1')], ['plugin', 'version']
    )

    mocked_spinner.assert_not_called()


@patch('forge.forge.Halo')
@patch('forge.forge.tabulate')
@patch('os.listdir')
def test_list_plugins_no_plugins_installed(mocked_listdir, mocked_tabulate, mocked_spinner):
    forge.PLUGIN_PATH = os.path.join('home', 'user', '.forge', 'venvs')

    fake_config_jsons = []

    with patch("builtins.open", multi_mock_open(*fake_config_jsons)):
        forge.list_plugins()

    mocked_tabulate.assert_not_called()
    assert mocked_spinner.mock_calls[1] == call().warn('No forge plugins installed yet! - Run forge --help for help')
