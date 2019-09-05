from git import Repo
from git import Git

class PluginPuller:


    def clone_plugin(self, repo_url, plugin_name, branch_name='dev'):
        return Repo.clone_from(repo_url, '/usr/local/etc/forge/plugins/' + plugin_name, branch=branch_name)

    def pull_plugin(repo_location, branch_name='dev'):
        return Git(repo_location).pull('origin', branch_name)

