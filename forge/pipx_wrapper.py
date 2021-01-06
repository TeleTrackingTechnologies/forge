""" Wrapper around pipx for Forge plugin management """


import re
from subprocess import PIPE, CalledProcessError, Popen
from typing import List, Tuple

from halo import Halo

from .exceptions import (PluginManagementFatalException,
                         PluginManagementWarnException)

DOTS = {
    "interval": 80,
    "frames": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
}


def make_spinner(text: str) -> Halo:
    """ Creates uniform stylized Halo spinner """
    return Halo(
        text=text,
        spinner=DOTS,
        color='blue'
    )


def determine_is_fatal_error(current_error_message: str) -> bool:
    """ Determine if a pipx error message is truly fatal """
    acceptable_error_messages = [
        '(_copy_package_apps:66):   Overwriting file',
        '(_symlink_package_apps:95): Same path'
    ]

    for message in acceptable_error_messages:
        if message in current_error_message:
            return False

    return True


def run_command(command: List[str]) -> Tuple[str, str]:
    """ Wrapper to simplify handling subprocess commands """
    try:
        process = Popen(command, stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()

        if process.returncode and determine_is_fatal_error(current_error_message=stderr.decode()):
            raise PluginManagementFatalException(stderr.decode())

        return stdout.decode(), stderr.decode()

    except CalledProcessError as err:
        raise PluginManagementFatalException(err) from None


def update_pipx(name: str, extra_args: List[str]) -> None:
    """ Installs a plugin to pipx """
    command = f'pipx upgrade {name} --verbose'
    pretty_name = name.replace('forge-', '', 1)

    with make_spinner(text=f'Updating plugin: [{pretty_name}]...') as spinner:
        try:
            stdout, stderr = run_command(command.split() + extra_args)

            if 'Package is not installed' in stderr:
                spinner.warn('Plugin not installed! Cannot update!')
                raise PluginManagementWarnException()

            update_message = _extract_update_details(stdout)

            spinner.succeed(update_message)

        except PluginManagementFatalException as err:
            spinner.fail(f'Something went wrong!\n{str(err)}')
            raise PluginManagementFatalException from None


def install_to_pipx(source: str, extra_args: List[str]) -> None:
    """ Installs a plugin to pipx """
    command = f'pipx install {source} --verbose'

    with make_spinner(text='Installing plugin...') as spinner:
        try:
            stdout, _ = run_command(command.split() + extra_args)

            if 'already seems to be installed' in stdout:
                spinner.warn('Plugin already installed!')
                raise PluginManagementWarnException()

            plugin_name, package, python_version = _extract_result_details(stdout)

            spinner.succeed(f'Installed plugin: [{plugin_name}] [{package}] [{python_version}]!')

        except PluginManagementFatalException as err:
            spinner.fail(f'Something went wrong!\n{str(err)}')
            raise PluginManagementFatalException from None


def uninstall_from_pipx(plugin_name: str, extra_args: List[str]) -> str:
    """ Installs a plugin to pipx """
    command = f'pipx uninstall {plugin_name} --verbose'

    with make_spinner(text=f'Uninstalling plugin: [{plugin_name}]...') as spinner:
        try:
            stdout, _ = run_command(command.split() + extra_args)

            if f'Nothing to uninstall for {plugin_name}' in stdout:
                spinner.warn(f'Plugin {plugin_name} not installed!')
                raise PluginManagementWarnException()

            spinner.succeed(f'Uninstalled plugin: [{plugin_name}]!')

            return plugin_name

        except PluginManagementFatalException as err:
            spinner.fail(f'Something went wrong!\n{str(err)}')
            raise PluginManagementFatalException from None


def _extract_result_details(pipx_output: str) -> Tuple[str, str, str]:
    """ Extracts name and version from pipx's stdout """
    match = re.search(r'installed package(.*),(.*)\n.*\n.*?-(.*)', pipx_output)
    if match:
        package, python_version, plugin_name = map(str.strip, match.groups())

        return plugin_name.replace('.exe', ''), package, python_version

    raise PluginManagementFatalException('Failed to find package information install log!')


def _extract_update_details(pipx_output: str) -> str:
    """ Extracts update message from pipx's stdout """

    match = re.findall(r'(.*forge-.*)\(', pipx_output)

    if match:
        return str(match[-1].strip().replace('forge-', '', 1))

    raise PluginManagementFatalException('Failed to find update information from update log!')
