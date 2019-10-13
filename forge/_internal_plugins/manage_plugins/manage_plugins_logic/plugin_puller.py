""" Plugin Puller """
import subprocess
from pathlib import Path
from git import Repo
from git import Git
from colorama import Fore

class PluginPuller:
    """ Plugin Puller Class Def """
    def __init__(self, config_handler):
        self.config_handler = config_handler

    def pull_plugin(self, plugin_name, branch_name='dev'):
        """Updates plugin by executing a git pull from its install location"""
        repo = str(Path(f'{self.config_handler.get_plugin_install_location()}/{plugin_name}'))
        repo = Git(repo).pull('origin', branch_name)
        self._install_dependencies(plugin_name)
        return repo


    def clone_plugin(self, repo_url, plugin_name, branch_name='dev'):
        """ Clone Plugin From Git """
        repo = Repo.clone_from(
            repo_url,
            str(Path(f'{self.config_handler.get_plugin_install_location()}/{plugin_name}')),
            branch=branch_name
        )
        self._install_dependencies(plugin_name)
        return repo

    def _install_dependencies(self, name):
        print(Fore.GREEN + '\n' + "Installing plugin dependencies...")
        plugin_location = str(Path(f'{self.config_handler.get_plugin_install_location()}/{name}'))
        with open(Path(f'{plugin_location}/requirements.txt')) as requirements_file:
            for line in requirements_file:
                subprocess.call(['pip3', 'install', '-U', line])
