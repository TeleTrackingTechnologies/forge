from git import Repo


class PluginPuller:

    def clone_plugin(repo_url, plugin_name):
        return Repo.clone_from(repo_url, '/usr/local/etc/forge/plugins/' + plugin_name, branch='dev')
