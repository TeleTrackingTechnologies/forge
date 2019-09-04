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
        p = Process(target=self.show_spinner)
        p.start()

        name = self.pull_name_from_url(parsed_args.repo_url)
        if name is None:
            self.handle_error('Repository name should be in the form of forge-[alphanumeric name]', p)

        print("Pulling plugin source...")
        try:
            repo = self.pull_plugin(parsed_args.repo_url, name)
            if repo.bare:
                self.handle_error('Plugin repository contained no source code...', p)
        except GitCommandError as err:
            self.handle_error(f'Could not pull plugin {err}', p)

        print(Fore.GREEN + '\n' + "Pulled plugin source, configuring for use...")
        self.write_plugin_to_ini(name, parsed_args.repo_url)
        p.terminate()
        print(Fore.GREEN + '\n' + 'Plugin ready for use!')


    def init_arg_parser(self):
        parser = argparse.ArgumentParser(prog='forge manage-plugins')
        parser.add_argument('-p', '--plugin', action='store', dest='repo_url', required=True,
                            help='Url to git repo containing plugin source.')
        return parser

    def handle_error(self, message, spinner):
        init(autoreset=True)
        spinner.terminate()
        print(Fore.RED + '\n' + message)
        deinit()
        sys.exit(1)

    def pull_plugin(self, url, name):
        return PluginPuller.clone_plugin(url, name)

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