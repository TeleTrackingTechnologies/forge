""" Manage Plugins Internally """
import argparse
import os
import re
import subprocess
import sys
from typing import Any

from colorama import Fore, deinit, init
from forge.config.config_handler import ConfigHandler
from git import GitCommandError, GitCommandNotFound, Repo
from halo import Halo

from .command_line_parser import init_arg_parser
from .manage_plugin_exceptions import (PluginManagementFatalException,
                                       PluginManagementWarnException)
from .plugin_puller import PluginPuller


class ManagePlugins:
    """ Manage Plugins """

    def __init__(self, plugin_puller: PluginPuller, config_handler: ConfigHandler) -> None:
        self.arg_parser = init_arg_parser()
        self.plugin_puller = plugin_puller
        self.config_handler = config_handler

    def execute(self, args: list) -> None:
        """ Execute """
        parsed_args = self.arg_parser.parse_args(args=args)
        self.validate_args(parsed_args=parsed_args)

        init(autoreset=True)

        try:
            if parsed_args.action_type == 'ADD':
                self._do_add(parsed_args)
            elif parsed_args.action_type == 'UPDATE':
                self._do_update(parsed_args)
            elif parsed_args.action_type == 'INIT':
                self._do_init(parsed_args)

        except PluginManagementFatalException:
            sys.exit(1)
        except PluginManagementWarnException:
            sys.exit(0)

        finally:
            deinit()

    @staticmethod
    def pull_name_from_url(url: str) -> Any:
        """ Extract Plugin Name from Git URL """
        match = re.search(r'[\s]*\/(forge(?:-[A-Za-z1-9]*)+)[\s]*', url)
        if not match:
            handle_error('Repository name should be in the form of forge-[alphanumeric name]')
        return match.group(1)

    def validate_args(self, parsed_args: argparse.Namespace) -> None:
        """Validates passed in args, the presence of some args makes other args required."""
        action = parsed_args.action_type
        if action == 'ADD':
            self._validate_add_action(args=parsed_args)
        elif action is None:
            handle_error('Please provide an action with -a, -u or -i')

    @staticmethod
    def _validate_add_action(args: argparse.Namespace) -> None:
        if args.repo_url is None:
            handle_error('Cant add plugin without providing url!')

    def _clone_plugin_step(self, name, args) -> None:
        """ Clones plugin source code into forge folder """
        with Halo(text='Cloning source code...', spinner='dots', color='blue') as spinner:
            try:
                repo = self.plugin_puller.clone_plugin(repo_url=args.repo_url, plugin_name=name, branch_name=args.branch_name)
                spinner.succeed("Cloned plugin source code!")

            except PluginManagementFatalException as err:
                spinner.fail('Could not clone plugin! ' + str(err))
                raise err from None

            except PluginManagementWarnException as err:
                spinner.warn(str(err))
                raise err from None

    def _configure_plugin_step(self, args) -> None:
        """ Configures plugin for use by forge """
        name = self.pull_name_from_url(url=args.repo_url)
        with Halo(text='Configuring plugin for use...', spinner='dots', color='blue') as spinner:
            self.config_handler.write_plugin_to_conf(
                name=name,
                url=args.repo_url
            )
            spinner.succeed(f"Plugin configured!")

    def _pull_plugin_step(self, name: str, args: argparse.Namespace) -> None:
        """ Pulls plugin source code into forge folder """

        with Halo(text=f'Updating plugin: [{name}]...', spinner='dots', color='blue') as spinner:
            try:
                repo = self.plugin_puller.pull_plugin(plugin_name=name, branch_name=args.branch_name)
                spinner.succeed(text=f"Plugin: [{name}] updated!")

            except PluginManagementFatalException as err:
                spinner.fail(f'Could not update plugin: [{name}]! {str(err)}')
                raise err from None

            except PluginManagementWarnException:
                spinner.succeed(f'Plugin: [{name}] already up to date!')

    def _install_dependencies(self) -> None:
        """ Installs all dependencies required by all plugins """
        with Halo(text='Installing plugin dependencies...', spinner='dots', color='blue') as spinner:
            for plugin_path in self.config_handler.get_plugins():
                req_file = os.path.join(plugin_path, 'requirements.txt')
                if os.path.exists(req_file):
                    with open(os.devnull, 'wb') as devnull:
                        subprocess.check_call(f'{sys.executable} -m pip install -r {req_file}'.split(), stdout=devnull, stderr=subprocess.STDOUT)
            spinner.succeed(f"Plugin dependencies installed!")

    def _do_add(self, args: argparse.Namespace) -> None:
        print('Installing plugin...')

        name = self.pull_name_from_url(url=args.repo_url)

        self._clone_plugin_step(name=name, args=args)
        self._configure_plugin_step(args=args)
        self._install_dependencies()

        with Halo(text='Finishing up...', spinner='dots', color='blue') as spinner:
            spinner.succeed('Plugin installed and ready for use!')

    def _do_update(self, args: argparse.Namespace) -> None:
        print('Updating plugins...')
        if args.plugin_name:
            self._pull_plugin_step(name=args.plugin_name, args=args)
        else:
            for name, url in self.config_handler.get_plugin_entries():
                args.repo_url = url
                self._pull_plugin_step(name=name, args=args)

        with Halo(text='Finishing up...', spinner='dots', color='blue') as spinner:
            spinner.succeed('Updated plugins!')

    def _do_init(self, args: argparse.Namespace):
        print('Initializing plugins...')

        for name, url in self.config_handler.get_plugin_entries():
            args.repo_url = url
            self._clone_plugin_step(name=name, args=args)

        self._install_dependencies()

        with Halo(text='Finishing up...', spinner='dots', color='blue') as spinner:
            spinner.succeed('Initialized plugins!')


def write_failure_message(message: str) -> None:
    """ Writes message in red color for errors """
    print(Fore.RED + '\n' + message)


def handle_error(message: str) -> None:
    """ Class Level Error Handling """
    write_failure_message(message)
    raise PluginManagementFatalException(message)
