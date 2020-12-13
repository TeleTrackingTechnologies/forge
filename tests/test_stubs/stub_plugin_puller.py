# pylint: disable=all
from git import GitCommandError
from forge._internal_plugins.manage_plugins.manage_plugins_logic.plugin_puller import PluginPuller


class StubPluginPuller(PluginPuller):
    def __init__(self, config_handler):
        super().__init__(config_handler)

    @staticmethod
    def pull_plugin(plugin_name, branch_name='dev'):
        """ stub for pull_plugin of PluginPuller."""
        return {}

    @staticmethod
    def clone_plugin(repo_url, plugin_name, branch_name='dev'):
        """ Clone Plugin From Git """
        return StubRepo()


class StubRepo:
    bare = False


class StubPluginPullerWithError(PluginPuller):
    def __init__(self, config_handler):
        super().__init__(config_handler)

    @staticmethod
    def pull_plugin(plugin_name, branch_name='dev'):
        """stub method to raise error on pull."""
        raise GitCommandError('test', None)
