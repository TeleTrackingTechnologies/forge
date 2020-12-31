""" Entrypoint for Forge """


import sys

from forge.cli import forge_cli, inject_forge_plugins
from forge.exceptions import (PluginManagementFatalException,
                              PluginManagementWarnException)


def main() -> None:
    """ Error-handled entry point for cli entry point """
    try:
        inject_forge_plugins()
        forge_cli()  # pylint: disable=no-value-for-parameter
    except PluginManagementFatalException:
        sys.exit(1)
    except PluginManagementWarnException:
        sys.exit(0)
