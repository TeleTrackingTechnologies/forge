class StubPluginPuller:
    @staticmethod
    def pull_plugin(repo_location, branch_name='dev'):
        """ Executes a 'git pull' on the provided repo."""
        return {}

    @staticmethod
    def clone_plugin(repo_url, plugin_name, branch_name='dev'):
        """ Clone Plugin From Git """
        return StubRepo()


class StubRepo:
    bare = False
