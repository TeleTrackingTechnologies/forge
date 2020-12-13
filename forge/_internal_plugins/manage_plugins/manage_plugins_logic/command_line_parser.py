""" Command Line Parser for Manage Plugins """

import argparse


def init_arg_parser() -> argparse.ArgumentParser:
    """ Initialize Argument Parser """
    parser = argparse.ArgumentParser(
        prog='forge manage-plugins',
        description='Tool to allow users to configure their '
                    'anvil installations with plugins. Provides '
                    'the ability to add plugins via a repo reference '
                    'and the ability to update all plugins currently installed. '
                    'See -h for more information.')
    parser.add_argument('-a', '--add',
                        action='store_const',
                        dest='action_type',
                        const='ADD',
                        required=False,
                        help='Add a new plugin')

    parser.add_argument('-u', '--update',
                        action='store_const',
                        dest='action_type',
                        const='UPDATE',
                        required=False,
                        help='Updates named plugin (via -n) or all plugins if -n not '
                        'provided')
    parser.add_argument('-i', '--init',
                        action='store_const',
                        dest='action_type',
                        const='INIT',
                        required=False,
                        help='Initializes Forge based on an existing plugin conf.ini.')
    parser.add_argument('-r', '--repo',
                        action='store',
                        dest='repo_url',
                        required=False,
                        help='Url to git repo containing plugin source. '
                        'NOTE it must refer to the clone URL, not the browser URL.')
    parser.add_argument('-b', '--branch',
                        action='store',
                        dest='branch_name',
                        required=False,
                        help='Optionally pass the branch name for the plugin.')
    parser.add_argument('-n', '--name',
                        action='store',
                        dest='plugin_name',
                        required=False,
                        help='The exact name of the plugin.')
    return parser
