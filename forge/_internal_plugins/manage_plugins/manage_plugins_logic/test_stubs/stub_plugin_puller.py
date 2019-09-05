from git import GitCommandError


class StubPluginPuller:
    @staticmethod
    def pull_plugin(repo_location, branch_name='dev'):
        """ stub for pull_plugin of PluginPuller."""
        return {}

    @staticmethod
    def clone_plugin(repo_url, plugin_name, branch_name='dev'):
        """ Clone Plugin From Git """
        return StubRepo()


class StubRepo:
    bare = False


class StubPluginPullerWithError:
    @staticmethod
    def pull_plugin(repo_location, branch_name='dev'):
        """stub method to raise error on pull."""
        raise GitCommandError('test', None)
