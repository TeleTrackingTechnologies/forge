""" Manage Plugins Internally """
import argparse
import sys
import itertools
import re
from multiprocessing import Process
from colorama import init, deinit, Fore
from git import GitCommandError, GitCommandNotFound, Repo
from .plugin_puller import PluginPuller
from typing import Iterator, Any, List
from forge.config.config_handler import ConfigHandler



class ManagePlugins:
    """ Manage Plugins """
    def __init__(self, plugin_puller: PluginPuller, config_handler: ConfigHandler) -> None:
        self.arg_parser = self.init_arg_parser()
        self.plugin_puller = plugin_puller
        self.config_handler = config_handler

    def execute(self, args: list) -> None:
        """ Execute """
        parsed_args = self.arg_parser.parse_args(args=args)
        self.validate_args(parsed_args=parsed_args)

        spinner_process = Process(target=self.show_spinner)
        spinner_process.start()
        if parsed_args.action_type == 'ADD':
            self._do_add(parsed_args, spinner_process)
        elif parsed_args.action_type == 'UPDATE':
            self._do_update(parsed_args, spinner_process)
        elif parsed_args.action_type == 'INIT':
            self._do_init(parsed_args, spinner_process)

    @staticmethod
    def init_arg_parser() -> argparse.ArgumentParser:
        """ Initialize Argument Parser """
        parser = argparse.ArgumentParser(
            prog='forge manage-plugins',
            description='Tool to allow users to configure their '
                        'anvil installations with plugins. Provides '
                        'the ability to add plugins via a repo reference '
                        'and the ability to update all plugins currently installed. '
                        'See -h for more information.')
        parser.add_argument('-a', '--add',
                            action='store_const',
                            dest='action_type',
                            const='ADD',
                            required=False,
                            help='Add a new plugin')

        parser.add_argument('-u', '--update',
                            action='store_const',
                            dest='action_type',
                            const='UPDATE',
                            required=False,
                            help='Updates named plugin (via -n) or all plugins if -n not '
                                 'provided')
        parser.add_argument('-i', '--init',
                            action='store_const',
                            dest='action_type',
                            const='INIT',
                            required=False,
                            help='Initializes Forge based on an existing plugin conf.ini.')
        parser.add_argument('-r', '--repo',
                            action='store',
                            dest='repo_url',
                            required=False,
                            help='Url to git repo containing plugin source. '
                                 'NOTE it must refer to the clone URL, not the browser URL.')
        parser.add_argument('-b', '--branch',
                            action='store',
                            dest='branch_name',
                            required=False,
                            help='Optionally pass the branch name for the plugin.')
        parser.add_argument('-n', '--name',
                            action='store',
                            dest='plugin_name',
                            required=False,
                            help='The exact name of the plugin.')
        return parser

    @staticmethod
    def handle_error(message: str, spinner: Process) -> None:
        """ Class Level Error Handling """
        init(autoreset=True)
        spinner.terminate()
        print(Fore.RED + '\n' + message)
        deinit()
        sys.exit(1)

    def pull_plugin(self, url: str, name: str, branch_name: str) -> Repo:
        """ Pull Plugin from Git """
        return self.plugin_puller.clone_plugin(url, name, branch_name)

    @staticmethod
    def show_spinner() -> None:
        """ Graphical Spinner on CLI """
        spinner = itertools.cycle('-/|\\')
        while True:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')

    @staticmethod
    def pull_name_from_url(url: str) -> Any:
        """ Extract Plugin Name from Git URL """
        match = re.search(r'[\s]*\/(forge-[A-Za-z1-9]+)[\s]*', url)

        if match:
            return match.group(1)

        return None

    def validate_args(self, parsed_args: argparse.Namespace) -> None:
        """Validates passed in args, the presence of some args makes other args required."""
        action = parsed_args.action_type
        if action == 'ADD':
            self._validate_add_action(args=parsed_args)
        elif action is None:
            print(Fore.RED + '\n' +
                  'Please provide an action with -a, -u or -i')
            sys.exit(1)

    @staticmethod
    def _validate_add_action(args: argparse.Namespace) -> None:
        if args.repo_url is None:
            print(Fore.RED + '\n' +
                  'Cant add plugin without providing url!')
            sys.exit(1)

    def _do_add(self, args: argparse.Namespace, spinner: Process) -> None:
        name = self.pull_name_from_url(url=args.repo_url)
        if name is None:
            self.handle_error(
                message='Repository name should be in the form of forge-[alphanumeric name]',
                spinner=spinner
            )
        repo = None
        print("Pulling plugin source...")
        try:
            repo = self.pull_plugin(url=args.repo_url, name=name, branch_name=args.branch_name)
            if repo.bare:
                self.handle_error(
                    message='Plugin repository contained no source code...',
                    spinner=spinner
                )
        except GitCommandError as err:
            self.handle_error(
                message=f'Could not pull plugin {err}',
                spinner=spinner
            )
        print(Fore.GREEN + '\n' + "Pulled plugin source, configuring for use...")
        self.config_handler.write_plugin_to_conf(
            name=name,
            url=args.repo_url
        )
        spinner.terminate()
        print(Fore.GREEN + '\n' + 'Plugin ready for use!')

    def _do_update(self, args: argparse.Namespace, spinner: Process) -> None:
        if args.plugin_name:
            try:
                self.plugin_puller.pull_plugin(
                    plugin_name=args.plugin_name,
                    branch_name=args.branch_name
                )
                print(Fore.GREEN + '\n' + 'Plugin updated!')
            except GitCommandError as err:
                self.handle_error(
                    message=f'Could not update plugin {err}',
                    spinner=spinner
                )
            except GitCommandNotFound as err:
                self.handle_error(
                    message=f'Could not update plugin, most' \
                    'likely caused by providing an invalid name.',
                    spinner=spinner
                )
        else:
            for name in self.config_handler.get_plugin_entries():
                print(f'Updating {name}...')
                try:
                    self.plugin_puller.pull_plugin(
                        plugin_name=name,
                        branch_name=args.branch_name
                    )
                except GitCommandError as err:
                    self.handle_error(
                        message=f'Could not update plugin {name} :  {err}',
                        spinner=spinner
                    )
        spinner.terminate()
        print(Fore.GREEN + '\n' + 'Plugin(s) updated!')

    def _do_init(self, args: argparse.Namespace, spinner: Process):
        for(name, url) in self.config_handler.get_plugin_entries():
            print(f'Installing {name}...')
            try:
                self.plugin_puller.clone_plugin(
                    repo_url=url,
                    plugin_name=name,
                    branch_name=args.branch_name
                )
            except GitCommandError as err:
                self.handle_error(
                    message=f'Could not install plugin {name} :  {err}',
                    spinner=spinner
                )
        spinner.terminate()
        print(Fore.GREEN + '\n' + 'Plugins installed!')
