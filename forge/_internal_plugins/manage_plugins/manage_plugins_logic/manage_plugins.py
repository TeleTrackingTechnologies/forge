""" Manage Plugins Internally """
import argparse
import sys
import itertools
import re
from multiprocessing import Process
from colorama import init, deinit, Fore
from git import GitCommandError
from git import GitCommandNotFound


class ManagePlugins:
    """ Manage Plugins """
    def __init__(self, plugin_puller, config_handler):
        self.arg_parser = self.init_arg_parser()
        self.plugin_puller = plugin_puller
        self.config_handler = config_handler

    def execute(self, args):
        """ Execute """
        parsed_args = self.arg_parser.parse_args(args)
        self.validate_args(parsed_args)

        spinner_process = Process(target=self.show_spinner)
        spinner_process.start()
        if parsed_args.action_type == 'ADD':
            self._do_add(parsed_args, spinner_process)
        elif parsed_args.action_type == 'UPDATE':
            self._do_update(parsed_args, spinner_process)
        elif parsed_args.action_type == 'INIT':
            self._do_init(parsed_args, spinner_process)

    @staticmethod
    def init_arg_parser():
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
    def handle_error(message, spinner):
        """ Class Level Error Handling """
        init(autoreset=True)
        spinner.terminate()
        print(Fore.RED + '\n' + message)
        deinit()
        sys.exit(1)

    def pull_plugin(self, url, name, branch_name):
        """ Pull Plugin from Git """
        return self.plugin_puller.clone_plugin(url, name, branch_name)

    @staticmethod
    def show_spinner():
        """ Graphical Spinner on CLI """
        spinner = itertools.cycle('-/|\\')
        while True:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')

    @staticmethod
    def pull_name_from_url(url):
        """ Extract Plugin Name from Git URL """
        match = re.search(r'[\s]*\/(forge-[A-Za-z1-9]+)[\s]*', url)

        if match:
            return match.group(1)

        return None

    def validate_args(self, parsed_args):
        """Validates passed in args, the presence of some args makes other args required."""
        action = parsed_args.action_type
        if action == 'ADD':
            self._validate_add_action(parsed_args)
        elif action is None:
            print(Fore.RED + '\n' +
                  'Please provide an action with -a, -u or -i')
            sys.exit(1)

    @staticmethod
    def _validate_add_action(args):
        if args.repo_url is None:
            print(Fore.RED + '\n' +
                  'Cant add plugin without providing url!')
            sys.exit(1)

    def _do_add(self, args, spinner):
        name = self.pull_name_from_url(args.repo_url)
        if name is None:
            self.handle_error(
                'Repository name should be in the form of forge-[alphanumeric name]', spinner
            )

        print("Pulling plugin source...")
        try:
            repo = self.pull_plugin(args.repo_url, name, args.branch_name)
            if repo.bare:
                self.handle_error('Plugin repository contained no source code...', spinner)
        except GitCommandError as err:
            self.handle_error(f'Could not pull plugin {err}', spinner)

        print(Fore.GREEN + '\n' + "Pulled plugin source, configuring for use...")
        self.config_handler.write_plugin_to_conf(name, args.repo_url)
        spinner.terminate()
        print(Fore.GREEN + '\n' + 'Plugin ready for use!')

    def _do_update(self, args, spinner):
        if args.plugin_name:
            try:
                self.plugin_puller.pull_plugin(
                    f'/usr/local/etc/forge/plugins/{args.plugin_name}', args.branch_name
                )
                print(Fore.GREEN + '\n' + 'Plugin updated!')
            except GitCommandError as err:
                self.handle_error(f'Could not update plugin {err}', spinner)
            except GitCommandNotFound as err:
                self.handle_error(
                    f'Could not update plugin, most likely caused by providing an invalid name.'
                    , spinner
                )
        else:
            for name in self.config_handler.read_plugin_entries():
                print(f'Updating {name}...')
                try:
                    self.plugin_puller.pull_plugin(
                        f'/usr/local/etc/forge/plugins/{name}',
                        args.branch_name
                    )
                except GitCommandError as err:
                    self.handle_error(f'Could not update plugin {name} :  {err}', spinner)

        print(Fore.GREEN + '\n' + 'Plugin(s) updated!')
        spinner.terminate()

    def _do_init(self, args, spinner):
        for(name, url) in self.config_handler.read_plugin_entries():
            print(f'Installing {name}...')
            try:
                self.plugin_puller.clone_plugin(url, name, args.branch_name)
            except GitCommandError as err:
                self.handle_error(f'Could not install plugin {name} :  {err}', spinner)
        print(Fore.GREEN + '\n' + 'Plugins installed!')
        spinner.terminate()
