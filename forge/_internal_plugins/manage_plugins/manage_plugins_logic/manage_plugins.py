import argparse
from colorama import init, deinit, Fore
import sys
from multiprocessing import Process
import itertools
from git import GitCommandError
import re
from .plugin_puller import PluginPuller
import configparser


class AddPlugin:
    def __init__(self):
        self.arg_parser = self.init_arg_parser()

    def execute(self, args):
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



    def init_arg_parser(self):
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
        return parser

    def handle_error(self, message, spinner):
        init(autoreset=True)
        spinner.terminate()
        print(Fore.RED + '\n' + message)
        deinit()
        sys.exit(1)

    def pull_plugin(self, url, name, branch_name):
        return PluginPuller.clone_plugin(url, name, branch_name)

    def show_spinner(self):
        spinner = itertools.cycle('-/|\\')
        while True:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')

    def pull_name_from_url(self, url):
        match = re.search('[\s]*\/(forge-[A-Za-z1-9]+)[\s]*', url)

        if match:
            return match.group(1)
        else:
            return None


    def write_plugin_to_ini(self, name, url):
        config = configparser.ConfigParser()
        config.read('/usr/local/etc/forge/conf.ini')
        plugin_section = config['plugin-definitions']
        plugin_section[name] = url
        with open('/usr/local/etc/forge/conf.ini', 'w') as configfile:
            config.write(configfile)

    def validate_args(self, parsed_args):
        action = parsed_args.action_type
        if action is 'ADD':
            self._validate_add_action(parsed_args)
        elif action is None:
            print(Fore.RED + '\n' +
                  'Please provide an action with -a, -u or -i')
            sys.exit(1)

    def _validate_add_action(self, args):
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
        self.write_plugin_to_ini(name, args.repo_url)
        spinner.terminate()
        print(Fore.GREEN + '\n' + 'Plugin ready for use!')

    def _do_update(self, args, spinner):
        print('update')
        if args.repo_url:
            try:
                PluginPuller.pull_plugin(args.repo_url, args.branch_name)
                print(Fore.GREEN + '\n' + 'Plugin updated!')
            except GitCommandError as err:
                self.handle_error(f'Could not update plugin {err}', spinner)
        else:
            for (name, url) in self._get_config().items('plugin-definitions'):
                print(f'Updating {name}...')
                try:
                    PluginPuller.pull_plugin(f'/usr/local/etc/forge/plugins/{name}', args.branch_name)
                except GitCommandError as err:
                    self.handle_error(f'Could not update plugin {name} :  {err}', spinner)

        print(Fore.GREEN + '\n' + 'Plugin(s) updated!')
        spinner.terminate()

    def _do_init(self, args, spinner):
        print('init')

        spinner.terminate()

    def _get_config(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read('/usr/local/etc/forge/conf.ini')
        return config
