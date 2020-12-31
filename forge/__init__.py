""" Entrypoint for Forge """


import sys

from forge.cli import forge_cli
from forge.exceptions import (PluginManagementFatalException,
                              PluginManagementWarnException)


def main():
    """ Error-handled entry point for cli entry point """
    try:
        # Disable required here as context agrument is injected via a Click decorator
        forge_cli()  # pylint: disable=no-value-for-parameter
    except PluginManagementFatalException:
        sys.exit(1)
    except PluginManagementWarnException:
        sys.exit(0)
