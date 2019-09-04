from git import Repo


class PluginPuller:

    def clone_plugin(repo_url, plugin_name):
        return Repo.clone_from(repo_url, '/usr/local/etc/plugins/' + plugin_name, branch='master')
