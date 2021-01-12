""" Forge CLI """

from typing import List
from subprocess import Popen
import sys
import click

from forge import forge

from .pipx_wrapper import install_to_pipx, uninstall_from_pipx, update_pipx

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'],
                        ignore_unknown_options=True,
                        allow_extra_args=True)


def print_cmd_help(ctx: click.Context, param, value) -> None:  # type: ignore # pylint: disable=unused-argument
    """ Command help handler for dealing with nested commands """
    group = ctx.command
    parser = group.make_parser(ctx)
    global_opts, args, _ = parser.parse_args(args=sys.argv[1:])
    if global_opts.get("help") is True:
        click.echo(ctx.get_help())
        ctx.exit()

    if args:
        name, cmd, args = group.resolve_command(ctx, args)  # type: ignore
        help_names = cmd.get_help_option_names(ctx)

        if (set(args) & help_names) and name not in ('list', 'update', 'remove'):
            if name in forge.get_forge_plugin_command_names():
                run_forge_plugin([name, '-h'])
            else:
                cmd_ctx = click.Context(cmd, info_name=cmd.name, parent=ctx)
                click.echo(cmd_ctx.get_help())
                cmd_ctx.exit()


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-h",
    "--help",
    callback=print_cmd_help,
    is_flag=True
)
def forge_cli(help: str) -> None:  # pylint: disable=redefined-builtin, unused-argument
    """ Command Line Interface for Forge """
    if click.get_current_context().invoked_subcommand is None:
        forge.list_plugins()


@forge_cli.command(name='add')
@click.argument('pipx_args', nargs=-1, type=click.UNPROCESSED)
@click.option('-s', '--source',
              type=str,
              help='Source of plugin to install',
              metavar='PLUGIN_SOURCE',
              required=True)
def add_plugin(source: str, pipx_args: List[str]) -> None:
    """ Add plugin to Forge by providing source to be passed to PIPX """
    install_to_pipx(source=source, extra_args=list(pipx_args))


@forge_cli.command(name='update')
@click.argument('pipx_args', nargs=-1, type=click.UNPROCESSED)
@click.option('-n', '--name', type=str, help='Name of plugin(s) to update', metavar='PLUGIN_NAME')
def update_plugin(name: str, pipx_args: List[str]) -> None:
    """ Update plugin(s) """
    if name:
        if not name.startswith('forge-'):
            name = f'forge-{name}'
        update_pipx(name=name, extra_args=list(pipx_args))
    else:
        for plugin in forge.get_plugins():
            update_pipx(name=plugin['main_package']['package'], extra_args=list(pipx_args))


@forge_cli.command(name='remove')
@click.argument('pipx_args', nargs=-1, type=click.UNPROCESSED)
@click.option('-n', '--name', type=str, help='Name of plugin(s) to remove', metavar='PLUGIN_NAME')
def remove_plugin(name: str, pipx_args: List[str]) -> None:
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


def run_forge_plugin(command: List[str]) -> None:
    """ Forge Plugin """
    process = Popen(command)

    stdout, stderr = process.communicate()
    if stdout:
        click.echo(stdout.decode())

    if stderr:
        click.echo(stderr.decode())

    raise SystemExit(process.returncode)


def bind_plugin_command(plugin_name: str) -> None:
    """ Binds plugin command to click cli """
    @forge_cli.command(name=plugin_name,
                       context_settings=dict(
                           ignore_unknown_options=True,
                           allow_extra_args=True
                       ))  # pylint: disable=unused-variable
    def command() -> None:
        """ Plugin Entrypoint"""
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        run_forge_plugin([sys.argv[1]] + args)


def inject_forge_plugins() -> None:
    """ Inject all plugin command names into the click CLI """
    for command in forge.get_forge_plugin_command_names():
        bind_plugin_command(plugin_name=command)
