""" Plugin Puller """
from functools import wraps
from pathlib import Path

from git import Git, GitCommandError, GitCommandNotFound, Repo

from .manage_plugin_exceptions import (PluginManagementFatalException,
                                       PluginManagementWarnException)


def handle_git_errors(func):
    """ decorator to share error handling code between git operations """
    @wraps(func)
    def wrapper(*args, **kwargs):
        repo = None

        try:
            repo = func(*args, **kwargs)

        except GitCommandError as err:
            if 'already exists and is not an empty directory' in err.stderr:
                raise PluginManagementWarnException('Plugin already installed to forge!') from None
            failed_pull_message = f'Failed to pull source code! {err.stderr}'
            raise PluginManagementFatalException(failed_pull_message) from None

        except GitCommandNotFound as err:
            failed_pull_message = f'Failed to pull source code! {err.stderr}'
            raise PluginManagementFatalException(failed_pull_message) from None

        if not isinstance(repo, Repo):
            raise PluginManagementWarnException('Plugin already up to date!') from None
        if repo.bare:
            raise PluginManagementFatalException('Given repository has no data!') from None
        return repo

    return wrapper


class PluginPuller:
    """ Plugin Puller Class """

    def __init__(self, config_handler):
        self.config_handler = config_handler

    @handle_git_errors
    def pull_plugin(self, plugin_name, branch_name='dev') -> Repo:
        """Updates plugin by executing a git pull from its install location"""
        repo = str(Path(f'{self.config_handler.get_plugin_install_location()}/{plugin_name}'))
        repo = Git(repo).pull('origin', branch_name)

        return repo

    @handle_git_errors
    def clone_plugin(self, repo_url, plugin_name, branch_name='dev') -> Repo:
        """ Clone Plugin From Git """
        repo = Repo.clone_from(
            repo_url,
            str(Path(f'{self.config_handler.get_plugin_install_location()}/{plugin_name}')),
            branch=branch_name
        )

        return repo
