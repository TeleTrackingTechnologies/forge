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
                raise PluginManagementWarnException('Plugin already installed to forge!')
            raise PluginManagementFatalException(f'Failed to pull source code! {err.stderr}')

        except GitCommandNotFound as err:
            raise PluginManagementFatalException(f'Failed to pull source code! {err.stderr}')

        if not isinstance(repo, Repo):
            raise PluginManagementWarnException('Plugin already up to date!')
        elif repo.bare:
            raise PluginManagementFatalException('Given repository has no data!')
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
