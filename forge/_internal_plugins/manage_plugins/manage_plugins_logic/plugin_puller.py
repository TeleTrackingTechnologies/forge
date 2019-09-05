""" Plugin Puller """
from git import Repo


class PluginPuller:
    """ Plugin Puller Class Def """

    @staticmethod
    def clone_plugin(repo_url, plugin_name):
        """ Clone Plugin From Git """
        return Repo.clone_from(
            repo_url, '/usr/local/etc/forge/plugins/' + plugin_name,
            branch='dev'
        )
