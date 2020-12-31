import pytest
from forge.cli import forge_cli
from mock import call, patch


@patch('forge.forge.list_plugins')
def test_cli_no_command(mock_pipx_list):
    mock_args = 'forge'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_list.assert_called_once_with()


@patch('forge.forge.list_plugins')
def test_cli_list(mock_pipx_list):
    mock_args = 'forge list'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_list.assert_called_once_with()


@patch('forge.cli.install_to_pipx')
def test_cli_add(mock_pipx_install):
    mock_args = 'forge add --source some-source'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_install.assert_called_once_with(source='some-source', extra_args=[])


@patch('forge.cli.install_to_pipx')
def test_cli_add_with_extra_args(mock_pipx_install):
    mock_args = 'forge add -s some-source arg1 val1 arg2 val2'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_install.assert_called_once_with(
        source='some-source',
        extra_args=['arg1', 'val1', 'arg2', 'val2']
    )


@patch('forge.cli.update_pipx')
def test_cli_update(mock_pipx_update):
    mock_args = 'forge update --name plugin-name'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_update.assert_called_once_with(name='forge-plugin-name', extra_args=[])


@patch('forge.cli.update_pipx')
def test_cli_update_with_extra_args(mock_pipx_update):
    mock_args = 'forge update -n plugin-name arg1 val1 arg2 val2 '.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_update.assert_called_once_with(
        name='forge-plugin-name',
        extra_args=['arg1', 'val1', 'arg2', 'val2']
    )


@patch('forge.cli.update_pipx')
@patch('forge.forge.get_plugins')
def test_cli_update_all_since_no_name_given(mock_get_plugins, mock_pipx_update):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge update'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_update.mock_calls = [
        call(name='forge-plugin1', extra_args=[]),
        call(name='forge-plugin2', extra_args=[])
    ]


@patch('forge.cli.update_pipx')
@patch('forge.forge.get_plugins')
def test_cli_update_all_since_no_name_given_with_extra_args(mock_get_plugins, mock_pipx_update):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge update arg1 val1'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    mock_pipx_update.mock_calls = [
        call(name='forge-plugin1', extra_args=['arg1', 'val1']),
        call(name='forge-plugin2', extra_args=['arg1', 'val1'])
    ]


@patch('forge.cli.uninstall_from_pipx')
def test_cli_remove(uninstall_from_pipx):
    mock_args = 'forge remove -n plugin-name'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    uninstall_from_pipx.assert_called_once_with(plugin_name='forge-plugin-name', extra_args=[])


@patch('forge.cli.uninstall_from_pipx')
def test_cli_remove_with_extra_args(uninstall_from_pipx):
    mock_args = 'forge remove -n plugin-name arg1 val1 arg2 val2 '.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    uninstall_from_pipx.assert_called_once_with(
        plugin_name='forge-plugin-name',
        extra_args=['arg1', 'val1', 'arg2', 'val2']
    )


@patch('forge.cli.uninstall_from_pipx')
@patch('forge.forge.get_plugins')
def test_cli_remove_all_since_no_name_given(mock_get_plugins, uninstall_from_pipx):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge remove'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    uninstall_from_pipx.mock_calls = [
        call(plugin_name='forge-plugin1', extra_args=[]),
        call(plugin_name='forge-plugin2', extra_args=[])
    ]


@patch('forge.cli.uninstall_from_pipx')
@patch('forge.forge.get_plugins')
def test_cli_remove_all_since_no_name_given_with_extra_args(mock_get_plugins, uninstall_from_pipx):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge remove arg1 val1'.split()
    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()
    uninstall_from_pipx.mock_calls = [
        call(plugin_name='forge-plugin1', extra_args=['arg1', 'val1']),
        call(plugin_name='forge-plugin2', extra_args=['arg1', 'val1'])
    ]
