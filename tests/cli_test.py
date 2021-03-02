import pytest
from forge.cli import forge_cli, run_forge_plugin, inject_forge_plugins
from mock import call, patch


@pytest.fixture()
def mock_pipx_list():
    with patch('forge.forge.list_plugins') as mock:
        yield mock


@pytest.fixture()
def mock_pipx_install():
    with patch('forge.cli.install_to_pipx') as mock:
        yield mock


@pytest.fixture()
def mock_pipx_update():
    with patch('forge.cli.update_pipx') as mock:
        yield mock


@pytest.fixture()
def mock_get_plugins():
    with patch('forge.forge.get_plugins') as mock:
        yield mock


@pytest.fixture()
def mock_uninstall_from_pipx():
    with patch('forge.cli.uninstall_from_pipx') as mock:
        yield mock


def test_cli_no_command(mock_pipx_list):
    mock_args = 'forge'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_pipx_list.assert_called_once_with()


def test_cli_list(mock_pipx_list):
    mock_args = 'forge list'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_pipx_list.assert_called_once_with()


def test_cli_add(mock_pipx_install):
    mock_args = 'forge add --source some-source'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_pipx_install.assert_called_once_with(source='some-source', extra_args=[])


def test_cli_add_with_extra_args(mock_pipx_install):
    mock_args = 'forge add -s some-source arg1 val1 arg2 val2'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_pipx_install.assert_called_once_with(
        source='some-source',
        extra_args=['arg1', 'val1', 'arg2', 'val2']
    )


def test_cli_update(mock_pipx_update):
    mock_args = 'forge update --name plugin-name'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_pipx_update.assert_called_once_with(name='forge-plugin-name', extra_args=[])


def test_cli_update_with_extra_args(mock_pipx_update):
    mock_args = 'forge update -n plugin-name arg1 val1 arg2 val2 '.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_pipx_update.assert_called_once_with(
        name='forge-plugin-name',
        extra_args=['arg1', 'val1', 'arg2', 'val2']
    )


def test_cli_update_all_since_no_name_given(mock_get_plugins, mock_pipx_update):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge update'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    assert mock_pipx_update.mock_calls == [
        call(name='forge-plugin1', extra_args=[]),
        call(name='forge-plugin2', extra_args=[])
    ]


def test_cli_update_all_since_no_name_given_with_extra_args(mock_get_plugins, mock_pipx_update):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge update arg1 val1'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    assert mock_pipx_update.mock_calls == [
        call(name='forge-plugin1', extra_args=['arg1', 'val1']),
        call(name='forge-plugin2', extra_args=['arg1', 'val1'])
    ]


def test_cli_remove(mock_uninstall_from_pipx):
    mock_args = 'forge remove -n plugin-name'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_uninstall_from_pipx.assert_called_once_with(plugin_name='forge-plugin-name', extra_args=[])


def test_cli_remove_with_extra_args(mock_uninstall_from_pipx):
    mock_args = 'forge remove -n plugin-name arg1 val1 arg2 val2 '.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_uninstall_from_pipx.assert_called_once_with(
        plugin_name='forge-plugin-name',
        extra_args=['arg1', 'val1', 'arg2', 'val2']
    )


def test_cli_remove_all_since_no_name_given(mock_get_plugins, mock_uninstall_from_pipx):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge remove'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    assert mock_uninstall_from_pipx.mock_calls == [
        call(plugin_name='forge-plugin1', extra_args=[]),
        call(plugin_name='forge-plugin2', extra_args=[])
    ]


def test_cli_remove_all_since_no_name_given_with_extra_args(mock_get_plugins, mock_uninstall_from_pipx):
    mock_get_plugins.return_value = [
        {"main_package": {"package": "forge-plugin1"}},
        {"main_package": {"package": "forge-plugin2"}}
    ]
    mock_args = 'forge remove arg1 val1'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    assert mock_uninstall_from_pipx.mock_calls == [
        call(plugin_name='forge-plugin1', extra_args=['arg1', 'val1']),
        call(plugin_name='forge-plugin2', extra_args=['arg1', 'val1'])
    ]


def test_cli_help_forge(mock_echo):
    mock_args = 'forge -h'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_echo.assert_called_once()
    assert str(mock_echo.mock_calls[0].args[0]).split('\n')[0] == 'Usage: forge [OPTIONS] COMMAND [ARGS]...'


@patch('forge.forge.get_forge_plugin_command_names')
def test_cli_help_forge_core_command(mock_command_names, mock_echo):

    mock_args = 'forge add -h'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        forge_cli()

    mock_echo.assert_called_once()
    assert str(mock_echo.mock_calls[0].args[0]).split('\n')[0] == 'Usage: forge add [OPTIONS] [PIPX_ARGS]...'


def test_run_forge_plugin(mock_popen, mock_echo):
    mock_process = mock_popen.return_value
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b'stdout', b'stderr')

    with pytest.raises(SystemExit):
        run_forge_plugin(['ls'])

    assert mock_echo.mock_calls == [call('stdout'), call('stderr')]


@patch('forge.forge.get_forge_plugin_command_names', return_value=['plugin1'])
@patch('forge.cli.run_forge_plugin')
def test_cli_help_forge_plugin_command(mock_run_forge_plugin, mock_command_names):
    mock_args = 'forge plugin1 -h'.split()

    with patch('sys.argv', mock_args), pytest.raises(SystemExit):
        inject_forge_plugins()
        forge_cli()

    mock_run_forge_plugin.assert_called_once_with(['plugin1', '-h'])
