"""Module used to perform actions against plugin configuration."""
import configparser


class PluginConfigHandler:
    """Module responsible for writing values to plugin config."""
    CONF_FILE_LOCATION = '/usr/local/etc/forge/conf.ini'

    def write_plugin_to_conf(self, name, url):
        """ Write Plugin Info to Config File """
        config = configparser.ConfigParser()
        config.read(self.CONF_FILE_LOCATION)
        plugin_section = config['plugin-definitions']
        plugin_section[name] = url
        with open(self.CONF_FILE_LOCATION, 'w') as configfile:
            config.write(configfile)

    def read_plugin_entries(self):
        """Reads installed plugin entries"""
        config = configparser.ConfigParser()
        config.sections()
        config.read(self.CONF_FILE_LOCATION)
        return config.items('plugin-definitions')
