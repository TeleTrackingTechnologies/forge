""" Forge CLI """


import click

from forge import forge

from .pipx_wrapper import install_to_pipx, uninstall_from_pipx, update_pipx

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
# @click.option('command')
def forge_cli(context: click.Context) -> None:
    """ Command Line Interface for Forge """
    if context.invoked_subcommand is None:
        forge.list_plugins()


@forge_cli.command(name='add',
                   context_settings=dict(
                       ignore_unknown_options=True,
                       allow_extra_args=True)
                   )
@click.argument('pipx_args', nargs=-1, type=click.UNPROCESSED)
@click.option('-s', '--source',
              type=str,
              help='Source of plugin to install',
              metavar='PLUGIN_SOURCE',
              required=True)
def add_plugin(source: str, pipx_args) -> None:
    """ Add plugin to Forge by providing source to be passed to PIPX """
    install_to_pipx(source=source, extra_args=list(pipx_args))


@forge_cli.command(name='update',
                   context_settings=dict(
                       ignore_unknown_options=True,
                       allow_extra_args=True)
                   )
@click.argument('pipx_args', nargs=-1, type=click.UNPROCESSED)
@click.option('-n', '--name', type=str, help='Name of plugin(s) to update', metavar='PLUGIN_NAME')
def update_plugin(name: str, pipx_args) -> None:
    """ Update plugin(s) """
    if name:
        if not name.startswith('forge-'):
            name = f'forge-{name}'
        update_pipx(name=name, extra_args=list(pipx_args))
    else:
        for plugin in forge.get_plugins():
            update_pipx(name=plugin['main_package']['package'], extra_args=list(pipx_args))


@forge_cli.command(name='remove',
                   context_settings=dict(
                       ignore_unknown_options=True,
                       allow_extra_args=True)
                   )
@click.argument('pipx_args', nargs=-1, type=click.UNPROCESSED)
@click.option('-n', '--name', type=str, help='Name of plugin(s) to remove', metavar='PLUGIN_NAME')
def remove_plugin(name: str, pipx_args) -> None:
    """ Remove plugin(s) """
    if name:
        if not name.startswith('forge-'):
            name = f'forge-{name}'
        uninstall_from_pipx(plugin_name=name, extra_args=list(pipx_args))
    else:
        for plugin in forge.get_plugins():
            uninstall_from_pipx(
                plugin_name=plugin['main_package']['package'],
                extra_args=list(pipx_args)
            )


@forge_cli.command(name='list')
def list_forge_plugins() -> None:
    """ List installed Forge plugins """
    forge.list_plugins()
