""" Handles operations on Forge conf.ini """
import os
import configparser
from pathlib import Path

CONF_HOME = str(Path(str(Path.home()) + '/.forge'))
CONFIG_FILE_PATH = str(Path(CONF_HOME + '/conf.ini'))

class ConfigHandler:
    """ Class that handles operations against Forge conf.ini """
    @staticmethod
    def init_conf_dir():
        """Initializes the conf directory for Forge"""
        if not os.path.exists(CONF_HOME):
            os.mkdir(CONF_HOME)

    def init_conf_file(self):
        """ Initializes the conifiguration file used by Forge """
        config = self._get_config_parser()
        if not os.path.exists(CONFIG_FILE_PATH):
            config['plugin-definitions'] = {}
            config['install-conf'] = {}
             # this is default plugin install location
            config['install-conf']['pluginlocation'] = str(Path(CONF_HOME + '/plugins'))
            with open(CONFIG_FILE_PATH, 'w') as conf_file:
                config.write(conf_file)


    @staticmethod
    def _get_config_parser():
        config_parser = configparser.ConfigParser()
        config_parser.read(CONFIG_FILE_PATH)
        return config_parser


    def get_plugin_install_location(self):
        """ Returns the configured location for plugin installations """
        return self._get_config_parser()['install-conf']['pluginlocation']


    def get_plugins(self):
        """ Parse Plugin Configuration File """
        config = self._get_config_parser()
        plugins = []
        for plugin_name in config['plugin-definitions']:
            plugins.append(str(Path(self.get_plugin_install_location() + '/' + plugin_name)))
        return plugins

    def get_plugin_entries(self):
        """ Parses all of the plugin entries currently installed."""
        config = self._get_config_parser()
        config.sections()
        return config.items('plugin-definitions')

    def write_plugin_to_conf(self, name, url):
        """ Write Plugin Info to Config File """
        config = self._get_config_parser()
        plugin_section = config['plugin-definitions']
        plugin_section[name] = url
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)
