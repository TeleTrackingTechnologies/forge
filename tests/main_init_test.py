import pytest
from mock import MagicMock, call, patch
from pprint import pprint

import forge


@patch('forge.ConfigHandler')
@patch('forge.PLUGIN_BASE')
def test_application_init(mock_plugin_base, mock_config):
    mock_plugin_base.make_plugin_source().list_plugins.return_value = ['a', 'a_logic', 'b', 'b_logic']

    fake_plugin = MagicMock()

    mock_plugin_base.make_plugin_source().load_plugin.return_value = fake_plugin

    app = forge.Application(name='forge', config_handler=mock_config())

    assert fake_plugin.mock_calls[0] == call.register(app)
    assert fake_plugin.mock_calls[1] == call.register(app)


@patch('forge.ConfigHandler')
@patch('forge.PLUGIN_BASE')
def test_execute_help(mock_plugin_base, mock_config):
    app = forge.Application(name='forge', config_handler=mock_config())

    app.print_help = MagicMock()

    app.execute(command='help', args=None)

    app.print_help.assert_called_once()


@patch('forge.ConfigHandler')
@patch('forge.PLUGIN_BASE')
def test_execute_plugin_not_installed(mock_plugin_base, mock_config):
    app = forge.Application(name='forge', config_handler=mock_config())

    app.registry = {
        'plugin1': 'help1',
        'plugin2': 'help2',
    }

    with pytest.raises(SystemExit) as raised_ex:
        app.execute(command='plugin3', args=None)

    assert raised_ex.value.code == 1


@patch('forge.ConfigHandler')
@patch('forge.PLUGIN_BASE')
def test_execute_plugin_no_args(mock_plugin_base, mock_config):
    app = forge.Application(name='forge', config_handler=mock_config())

    plugin1 = MagicMock()
    app.registry = {
        'plugin1': (plugin1, 'help1')
    }

    app.execute(command='plugin1', args=None)

    assert plugin1.mock_calls == [call(None)]


@patch('forge.ConfigHandler')
@patch('forge.PLUGIN_BASE')
def test_execute_plugin_with_args(mock_plugin_base, mock_config):
    app = forge.Application(name='forge', config_handler=mock_config())

    plugin1 = MagicMock()
    app.registry = {
        'plugin1': (plugin1, 'help1')
    }

    app.execute(command='plugin1', args=['-arg1', 'val1', '-arg2', 'val2'])

    assert plugin1.mock_calls == [call(['-arg1', 'val1', '-arg2', 'val2'])]


@patch('forge.Application')
@patch('forge.ConfigHandler')
def test_main_no_args(mock_config, mock_app):
    command = ''
    forge.main(args=command.split())

    assert mock_config.mock_calls == [
        call(
            home_dir_path=forge.CONF_HOME,
            file_path_dir=forge.CONFIG_FILE_PATH
        )
    ]

    assert mock_app.mock_calls == [
        call(name='forge', config_handler=mock_config()),
        call().execute('help', None)
    ]


@patch('forge.Application')
@patch('forge.ConfigHandler')
def test_main_with_args(mock_config, mock_app):
    command = 'plugin1 -arg1 val1'
    forge.main(args=command.split())

    assert mock_config.mock_calls == [
        call(
            home_dir_path=forge.CONF_HOME,
            file_path_dir=forge.CONFIG_FILE_PATH
        )
    ]

    assert mock_app.mock_calls == [
        call(name='forge', config_handler=mock_config()),
        call().execute('plugin1', ['-arg1', 'val1'])
    ]
