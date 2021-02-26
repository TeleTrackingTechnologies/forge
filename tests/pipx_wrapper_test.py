from subprocess import CalledProcessError

import pytest
from forge import pipx_wrapper
from forge.exceptions import (PluginManagementFatalException,
                              PluginManagementWarnException)
from mock import call, patch


def run_command_fail(*args, **kwargs):
    raise CalledProcessError(returncode=1, cmd=' '.join(args[0]))


@pytest.fixture()
def mock_run_command():
    with patch('forge.pipx_wrapper.run_command') as mock:
        yield mock


def test_run_command(mock_popen):
    mock_process = mock_popen.return_value
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b'stdout', b'stderr')

    stdout, stderr = pipx_wrapper.run_command(['ls'])

    assert stdout == 'stdout'
    assert stderr == 'stderr'


def test_run_command_fail_non_zero_exit_code(mock_popen):
    mock_process = mock_popen.return_value
    mock_process.returncode = 1
    mock_process.communicate.return_value = (b'stdout', b'stderr')

    with pytest.raises(PluginManagementFatalException):
        pipx_wrapper.run_command(['ls'])


def test_update_pipx(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('forge-plugin-name updated to some version(', '')
    pipx_wrapper.update_pipx('forge-plugin-name', [])

    mock_run_command.assert_called_once_with(['pipx', 'upgrade', 'forge-plugin-name', '--verbose'])

    mock_spinner.assert_has_calls([
        call(text='Updating plugin: [plugin-name]...',
             spinner={'interval': 80, 'frames': [
                 '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'
             ]},
             color='blue'),
        call().__enter__().succeed('plugin-name updated to some version')
    ], any_order=True)


def test_update_pipx_fail_no_update_message_matched(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('Some pipx output without update message', '')

    with pytest.raises(PluginManagementFatalException):
        pipx_wrapper.update_pipx('forge-plugin-name', [])

    mock_spinner.assert_has_calls([
        call().__enter__().fail('Something went wrong!\nFailed to find update information from update log!')
    ], any_order=True)


def test_update_pipx_warn_already_up_to_date(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('', 'Package is not installed')

    with pytest.raises(PluginManagementWarnException):
        pipx_wrapper.update_pipx('forge-plugin-name', [])

    mock_spinner.assert_has_calls([
        call().__enter__().warn('Plugin not installed! Cannot update!')
    ], any_order=True)


def test_install_to_pipx(mock_run_command, mock_spinner):

    pipx_output = """
        installed package forge-plugin-name-here,python-version
        yada
        forge-plugin-name-here
    """

    mock_run_command.return_value = (pipx_output, '')

    pipx_wrapper.install_to_pipx('some-source', [])

    mock_run_command.assert_called_once_with(['pipx', 'install', 'some-source', '--verbose'])

    assert mock_spinner.mock_calls[0].kwargs['text'] == 'Installing plugin...'

    mock_spinner.assert_has_calls([
        call().__enter__().succeed(
            'Installed plugin: [plugin-name-here] [forge-plugin-name-here] [python-version]!'
        )
    ])


def test_install_to_pipx_warn_plugin_already_installed(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('already seems to be installed', '')

    with pytest.raises(PluginManagementWarnException):
        pipx_wrapper.install_to_pipx('forge-plugin-name', [])

    mock_spinner.assert_has_calls([
        call().__enter__().warn('Plugin already installed!')
    ], any_order=True)


def test_install_pipx_fail_no_install_message_matched(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('', '')

    with pytest.raises(PluginManagementFatalException):
        pipx_wrapper.install_to_pipx('forge-plugin-name', [])

    mock_spinner.assert_has_calls([
        call().__enter__().fail('Something went wrong!\nFailed to find package information install log!')
    ], any_order=True)


def test_uninstall_from_pipx(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('', '')

    pipx_wrapper.uninstall_from_pipx('forge-plugin-name', [])

    mock_run_command.assert_called_once_with(['pipx', 'uninstall', 'forge-plugin-name', '--verbose'])
    assert mock_spinner.mock_calls[0].kwargs['text'] == 'Uninstalling plugin: [forge-plugin-name]...'

    mock_spinner.assert_has_calls([
        call().__enter__().succeed('Uninstalled plugin: [forge-plugin-name]!')
    ], any_order=True)


def test_uninstall_from_pipx_warn_plugin_not_installed(mock_run_command, mock_spinner):
    mock_run_command.return_value = ('Nothing to uninstall for forge-plugin-name', '')

    with pytest.raises(PluginManagementWarnException):
        pipx_wrapper.uninstall_from_pipx('forge-plugin-name', [])

    mock_spinner.assert_has_calls([
        call().__enter__().warn('Plugin forge-plugin-name not installed!')
    ], any_order=True)


def test_uninstall_from_pipx_fail_some_pipx_exception(mock_popen, mock_spinner):
    mock_popen.side_effect = run_command_fail

    with pytest.raises(PluginManagementFatalException):
        pipx_wrapper.uninstall_from_pipx('forge-plugin-name', [])

    mock_spinner.assert_has_calls([
        call().__enter__().fail(
            "Something went wrong!\nCommand 'pipx uninstall forge-plugin-name --verbose' returned non-zero exit status 1."
        )
    ], any_order=True)


@pytest.mark.parametrize("error_message,expected_result", [
    ("""
        yada
        (_symlink_package_apps:95): Same path
        yada
    """, False),
    ("""
        yada
        (_copy_package_apps:66):   Overwriting file
        yada
    """, False),
    ("""
        yada
        some none error log message
        yada
    """, True)
])
def test_determine_is_fatal_error(error_message, expected_result):
    assert pipx_wrapper.determine_is_fatal_error(error_message) == expected_result
