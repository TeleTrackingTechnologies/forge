""" Plugin Puller """
from git import Repo
from git import Git


class PluginPuller:
    """ Plugin Puller Class Def """

    @staticmethod
    def pull_plugin(repo_location, branch_name='dev'):
        """ Executes a 'git pull' on the provided repo."""
        return Git(repo_location).pull('origin', branch_name)

    @staticmethod
    def clone_plugin(repo_url, plugin_name, branch_name='dev'):
        """ Clone Plugin From Git """
        return Repo.clone_from(
            repo_url, '/usr/local/etc/forge/plugins/' + plugin_name,
            branch=branch_name
        )
