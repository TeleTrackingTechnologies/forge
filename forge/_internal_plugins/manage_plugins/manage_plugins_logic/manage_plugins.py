""" Manage Plugins Internally """
import argparse
import sys
import itertools
import re
import configparser
from multiprocessing import Process
from colorama import init, deinit, Fore
from git import GitCommandError
from .plugin_puller import PluginPuller


class AddPlugin:
    """ Add Plugin """
    def __init__(self):
        self.arg_parser = self.init_arg_parser()

    def execute(self, args):
        """ Execute """
        parsed_args = self.arg_parser.parse_args(args)
        process = Process(target=self.show_spinner)
        process.start()

        name = self.pull_name_from_url(parsed_args.repo_url)
        if name is None:
            self.handle_error(
                'Repository name should be in the form of forge-[alphanumeric name]',
                process
            )

        print("Pulling plugin source...")
        try:
            repo = self.pull_plugin(parsed_args.repo_url, name)
            if repo.bare:
                self.handle_error('Plugin repository contained no source code...', process)
        except GitCommandError as err:
            self.handle_error(f'Could not pull plugin {err}', process)

        print(Fore.GREEN + '\n' + "Pulled plugin source, configuring for use...")
        self.write_plugin_to_ini(name, parsed_args.repo_url)
        process.terminate()
        print(Fore.GREEN + '\n' + 'Plugin ready for use!')

    @staticmethod
    def init_arg_parser():
        """ Initialize Argument Parser """
        parser = argparse.ArgumentParser(prog='forge manage-plugins')
        parser.add_argument('-p', '--plugin', action='store', dest='repo_url', required=True,
                            help='Url to git repo containing plugin source.')
        return parser

    @staticmethod
    def handle_error(message, spinner):
        """ Class Level Error Handling """
        init(autoreset=True)
        spinner.terminate()
        print(Fore.RED + '\n' + message)
        deinit()
        sys.exit(1)

    @staticmethod
    def pull_plugin(url, name):
        """ Pull Plugin from Git """
        return PluginPuller.clone_plugin(url, name)

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

    @staticmethod
    def write_plugin_to_ini(name, url):
        """ Write Plugin Info to Config File """
        config = configparser.ConfigParser()
        config.read('/usr/local/etc/forge/conf.ini')
        plugin_section = config['plugin-definitions']
        plugin_section[name] = url
        with open('/usr/local/etc/forge/conf.ini', 'w') as configfile:
            config.write(configfile)
