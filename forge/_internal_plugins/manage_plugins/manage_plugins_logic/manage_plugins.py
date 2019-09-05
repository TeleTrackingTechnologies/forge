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

        p = Process(target=self.show_spinner)
        p.start()
        if parsed_args.action_type is 'ADD':
            self._do_add(parsed_args, p)
        elif parsed_args.action_type is 'UPDATE':
            self._do_update(parsed_args, p)
        elif parsed_args.action_type is 'INIT':
            self._do_init(parsed_args, p)

    @staticmethod
    def init_arg_parser():
        """ Initialize Argument Parser """
        parser = argparse.ArgumentParser(prog='forge manage-plugins')
        parser.add_argument('-a', '--add', action='store_const', dest='action_type', const='ADD', required=False,
                            help='Add a new plugin')
        parser.add_argument('-u', '--update', action='store_const', dest='action_type', const='UPDATE', required=False,
                            help='Updates a plugin if given a plugin ref or updates all installed if no specific ref is given')
        parser.add_argument('-i', '--init', action='store_const', dest='action_type', const='INIT', required=False,
                            help='Initializes Forge based on an existing plugin conf.ini.')
        parser.add_argument('-p', '--plugin', action='store', dest='repo_url', required=False,
                            help='Url to git repo containing plugin source.')
        parser.add_argument('-b', '--branch', action='store', dest='branch_name', required=False,
                            help='Optionally pass the branch name for the plugin.')
        parser.add_argument('-n', '--name', action='store', dest='plugin_name', required=False,
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
        action = parsed_args.action_type
        if action is 'ADD':
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
            self.handle_error('Repository name should be in the form of forge-[alphanumeric name]', spinner)

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
                self.plugin_puller.pull_plugin(f'/usr/local/etc/forge/plugins/{args.plugin_name}', args.branch_name)
                print(Fore.GREEN + '\n' + 'Plugin updated!')
            except GitCommandError as err:
                self.handle_error(f'Could not update plugin {err}', spinner)
            except GitCommandNotFound as err:
                self.handle_error(f'Could not update plugin, most likely caused by providing an invalid name.', spinner)
        else:
            for (name, url) in self.config_handler.read_plugin_entries():
                print(f'Updating {name}...')
                try:
                    self.plugin_puller.pull_plugin(f'/usr/local/etc/forge/plugins/{name}', args.branch_name)
                except GitCommandError as err:
                    self.handle_error(f'Could not update plugin {name} :  {err}', spinner)

        print(Fore.GREEN + '\n' + 'Plugin(s) updated!')
        spinner.terminate()

    @staticmethod
    def _do_init(args, spinner):
        print('init')

        spinner.terminate()
