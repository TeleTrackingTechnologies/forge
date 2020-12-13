import os

import pytest
from mock import patch, MagicMock, call

from git import Repo, GitCommandError, GitCommandNotFound


from forge._internal_plugins.manage_plugins.manage_plugins_logic.plugin_puller import PluginPuller
from forge._internal_plugins.manage_plugins.manage_plugins_logic.manage_plugin_exceptions import PluginManagementFatalException, PluginManagementWarnException
from test_stubs.stub_config_parser import StubPluginConfigHandler

MODULE_PATH = 'forge._internal_plugins.manage_plugins.manage_plugins_logic.plugin_puller'


@patch(f'{MODULE_PATH}.Repo.clone_from', return_value=MagicMock(spec=Repo, bare=False))
def test_clone_plugin(mock_clone):

    puller = PluginPuller(StubPluginConfigHandler())

    puller.clone_plugin('long_url', 'forge-some-plugin')

    print(mock_clone.mock_calls)

    assert mock_clone.mock_calls[0] == call('long_url', f'path.to.install{os.path.sep}forge-some-plugin', branch='dev')


@patch(f'{MODULE_PATH}.Git')
def test_pull_plugin(mock_git):

    puller = PluginPuller(StubPluginConfigHandler())

    mock_git.return_value.pull.return_value = MagicMock(spec=Repo, bare=False)

    puller.pull_plugin('forge-some-plugin')

    assert mock_git.mock_calls[0] == call(f'path.to.install{os.path.sep}forge-some-plugin')
    assert mock_git.mock_calls[1] == call().pull('origin', 'dev')


@patch(f'{MODULE_PATH}.Git')
def test_pull_plugin_bare_repo(mock_git):

    puller = PluginPuller(StubPluginConfigHandler())

    mock_git.return_value.pull.return_value = MagicMock(spec=Repo)

    with pytest.raises(PluginManagementFatalException) as raised_ex:
        puller.pull_plugin('forge-some-plugin')

    assert str(raised_ex.value) == 'Given repository has no data!'


@patch(f'{MODULE_PATH}.Git')
def test_pull_plugin_up_to_date(mock_git):

    puller = PluginPuller(StubPluginConfigHandler())

    mock_git.return_value.pull.return_value = MagicMock()

    with pytest.raises(PluginManagementWarnException) as raised_ex:
        puller.pull_plugin('forge-some-plugin')

    assert str(raised_ex.value) == 'Plugin already up to date!'


@patch(f'{MODULE_PATH}.Git')
def test_pull_plugin_command_not_found_error(mock_git):

    puller = PluginPuller(StubPluginConfigHandler())

    mock_git.return_value.pull.side_effect = GitCommandNotFound('command', 'cause')

    with pytest.raises(PluginManagementFatalException) as raised_ex:
        puller.pull_plugin('forge-some-plugin')

    assert str(raised_ex.value) == 'Failed to pull source code! '


@patch(f'{MODULE_PATH}.Git')
def test_pull_plugin_command_error(mock_git):

    puller = PluginPuller(StubPluginConfigHandler())

    mock_git.return_value.pull.side_effect = GitCommandError('command', 'cause')

    with pytest.raises(PluginManagementFatalException) as raised_ex:
        puller.pull_plugin('forge-some-plugin')

    assert str(raised_ex.value) == 'Failed to pull source code! '
