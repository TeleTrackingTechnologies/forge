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

    def pull_plugin(self, plugin_name, branch_name='dev') -> Repo:
        """Updates plugin by executing a git pull from its install location"""
        repo = str(Path(f'{self.config_handler.get_plugin_install_location()}/{plugin_name}'))
        repo = Git(repo).pull('origin', branch_name)
        return repo


    def clone_plugin(self, repo_url, plugin_name, branch_name='dev') -> Repo:
        """ Clone Plugin From Git """
        repo = Repo.clone_from(
            repo_url,
            str(Path(f'{self.config_handler.get_plugin_install_location()}/{plugin_name}')),
            branch=branch_name
        )
        return repo
