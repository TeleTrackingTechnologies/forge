import os

import pytest
from mock import patch, MagicMock, call


from forge._internal_plugins.manage_plugins.manage_plugins_logic.manage_plugins import ManagePlugins
from forge._internal_plugins.manage_plugins.manage_plugins_logic.manage_plugin_exceptions import PluginManagementFatalException, PluginManagementWarnException
from test_stubs.stub_plugin_puller import StubPluginPuller
from test_stubs.stub_config_parser import StubPluginConfigHandler
from test_stubs.stub_plugin_puller import StubPluginPullerWithError

MODULE_PATH = 'forge._internal_plugins.manage_plugins.manage_plugins_logic.manage_plugins'


def test_add_with_no_url_error():
    command = '-a'
    with pytest.raises(PluginManagementFatalException) as raised_ex:
        ManagePlugins(StubPluginPuller(StubPluginConfigHandler()), StubPluginConfigHandler()).execute(command.split())
    assert str(raised_ex.value) == 'Can\'t add plugin without providing url!'


def test_add_with_no_action_error():
    command = ''
    with pytest.raises(PluginManagementFatalException) as raised_ex:
        ManagePlugins(StubPluginPuller(StubPluginConfigHandler()), StubPluginConfigHandler()).execute(command.split())
    assert str(raised_ex.value) == 'Please provide an action with -a, -u or -i'


@patch(f'{MODULE_PATH}._write_failure_message')
def test_add_with_bad_repo_name_error(mocked_write_failure_message):
    command = '-a -r git@this_name-doesnt-start-with-forgedash.git'
    with pytest.raises(SystemExit) as raised_ex:
        ManagePlugins(StubPluginPuller(StubPluginConfigHandler()), StubPluginConfigHandler()).execute(command.split())
    mocked_write_failure_message.assert_called_with('Repository name should be in the form of forge-[alphanumeric name]')
    assert raised_ex.value.code == 1


@pytest.mark.parametrize("command,expected_branch", [
    ('-a -r git@bitbucket.org:tele/forge-some-plugin', None),
    ('-a -r git@bitbucket.org:tele/forge-some-plugin -b TheBranch', 'TheBranch')
])
@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_config_parser.StubPluginConfigHandler.write_plugin_to_conf')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.clone_plugin')
def test_do_add(mock_clone, mock_configure, mock_subprocess, mock_exists, command, expected_branch):
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    manager.execute(command.split())

    mock_clone.assert_called_once_with(
        repo_url='git@bitbucket.org:tele/forge-some-plugin',
        plugin_name='forge-some-plugin',
        branch_name=expected_branch
    )
    mock_configure.assert_called_once_with(name='forge-some-plugin', url='git@bitbucket.org:tele/forge-some-plugin')
    mock_subprocess.assert_called_once()

    _, *args = mock_subprocess.mock_calls[0].args[0]

    assert ' '.join(args) == fr'-m pip install -r forge-some-plugin{os.path.sep}requirements.txt'


@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.clone_plugin')
def test_do_init(mock_clone, mock_subprocess, mock_exists):
    command = '-i'
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    manager.execute(command.split())

    mock_clone.assert_called_once_with(
        repo_url='git@bitbucket.org:tele/forge-some-plugin',
        plugin_name='forge-some-plugin',
        branch_name=None
    )
    mock_subprocess.assert_called_once()

    _, *args = mock_subprocess.mock_calls[0].args[0]

    assert ' '.join(args) == fr'-m pip install -r forge-some-plugin{os.path.sep}requirements.txt'


@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.clone_plugin', side_effect=PluginManagementFatalException('Reason'))
@patch(f'{MODULE_PATH}.Halo')
def test_do_init_some_clone_fatal_error(mock_spinner, mock_clone, mock_subprocess, mock_exists):
    command = '-i'
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    mock_spinner.return_value.__enter__.return_value = MagicMock()

    with pytest.raises(SystemExit) as raised_ex:
        manager.execute(command.split())

    assert raised_ex.value.code == 1
    assert mock_spinner.mock_calls[0] == call(text='Cloning plugin: [forge-some-plugin]...', spinner='dots', color='blue')
    assert mock_spinner.mock_calls[2] == call().__enter__().fail('Could not clone plugin: [forge-some-plugin]! Reason')

    mock_clone.assert_called_once_with(
        repo_url='git@bitbucket.org:tele/forge-some-plugin',
        plugin_name='forge-some-plugin',
        branch_name=None
    )


@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.clone_plugin', side_effect=PluginManagementWarnException('Reason'))
@patch(f'{MODULE_PATH}.Halo')
def test_do_init_some_clone_warning_error(mock_spinner, mock_clone, mock_subprocess, mock_exists):
    command = '-i'
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    mock_spinner.return_value.__enter__.return_value = MagicMock()

    with pytest.raises(SystemExit) as raised_ex:
        manager.execute(command.split())

    assert raised_ex.value.code == 0
    assert mock_spinner.mock_calls[0] == call(text='Cloning plugin: [forge-some-plugin]...', spinner='dots', color='blue')
    assert mock_spinner.mock_calls[2] == call().__enter__().warn('Reason')

    mock_clone.assert_called_once_with(
        repo_url='git@bitbucket.org:tele/forge-some-plugin',
        plugin_name='forge-some-plugin',
        branch_name=None
    )


@pytest.mark.parametrize("command,expected_name", [
    ('-u', 'forge-some-plugin'),
    ('-u -n forge-named-plugin', 'forge-named-plugin')
])
@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.pull_plugin')
def test_do_update(mock_pull, mock_subprocess, mock_exists, command, expected_name):
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    manager.execute(command.split())

    mock_pull.assert_called_once_with(
        plugin_name=expected_name, branch_name=None
    )


@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.pull_plugin', side_effect=PluginManagementFatalException('Reason'))
@patch(f'{MODULE_PATH}.Halo')
def test_do_update_some_pull_error(mock_spinner, mock_pull, mock_subprocess, mock_exists):
    command = '-u'
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    mock_spinner.return_value.__enter__.return_value = MagicMock()

    with pytest.raises(SystemExit) as raised_ex:
        manager.execute(command.split())

    assert raised_ex.value.code == 1
    assert mock_spinner.mock_calls[0] == call(text='Updating plugin: [forge-some-plugin]...', spinner='dots', color='blue')
    assert mock_spinner.mock_calls[2] == call().__enter__().fail('Could not update plugin: [forge-some-plugin]! Reason')


@patch('os.path.exists')
@patch('subprocess.check_call')
@patch('test_stubs.stub_plugin_puller.StubPluginPuller.pull_plugin', side_effect=PluginManagementWarnException())
@patch(f'{MODULE_PATH}.Halo')
def test_do_update_already_up_to_date(mock_spinner, mock_pull, mock_subprocess, mock_exists):
    command = '-u'
    manager = ManagePlugins(
        StubPluginPuller(StubPluginConfigHandler()),
        StubPluginConfigHandler()
    )

    mock_spinner.return_value.__enter__.return_value = MagicMock()

    manager.execute(command.split())

    assert mock_spinner.mock_calls[0] == call(text='Updating plugin: [forge-some-plugin]...', spinner='dots', color='blue')
    assert mock_spinner.mock_calls[2] == call().__enter__().succeed('Plugin: [forge-some-plugin] already up to date!')
