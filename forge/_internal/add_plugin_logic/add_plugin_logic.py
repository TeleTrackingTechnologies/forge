import argparse
from ..plugin_puller.PluginPuller import PluginPuller
from colorama import init, deinit, Fore
import sys
from multiprocessing import Process
import itertools

class AddPlugin:
    def __init__(self):
        self.arg_parser = self.init_arg_parser()

    def execute(self, args):
        parsed_args = self.arg_parser.parse_args(args)
        print("Pulling plugin source...")
        p = Process(target=self.show_spinner)
        p.start()

        try:
            repo = self.pull_plugin(parsed_args)
            if repo.bare:
                self.handle_error('Plugin repository contained no source code...', p)
        # except:
        #     self.handle_error('Could not pull plugin...', p)

        print(Fore.GREEN + '\n' + "Pulled plugin source, configuring for use...")

        p.terminate()
        print(Fore.GREEN + '\n' + 'Plugin ready for use!')



    def init_arg_parser(self):
        parser = argparse.ArgumentParser(prog='forge add-plugin')
        parser.add_argument('-p', '--plugin', action='store', dest='repo_url', required=True,
                            help='Url to git repo containing plugin source.')
        parser.add_argument('-n', '--name', action='store', dest='plugin_name', required=True,
                            help='Name of the plugin you are adding')
        return parser

    def handle_error(self, message, spinner):
        init(autoreset=True)
        spinner.terminate()
        print(Fore.RED + '\n' + message)
        deinit()
        sys.exit(1)

    def pull_plugin(self, parsed_args):
        return PluginPuller.pull_plugin(parsed_args.repo_url, parsed_args.plugin_name), False

    def show_spinner(self):
        spinner = itertools.cycle('-/|\\')
        while True:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')
