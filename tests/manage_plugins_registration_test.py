from mock import MagicMock, call, patch

from forge._internal_plugins.manage_plugins import manage_plugins

MODULE_PATH = 'forge._internal_plugins.manage_plugins'


def test_help_text():
    assert manage_plugins.helptext() == "For managing plugins for use by forge."


def test_register():
    fake_app = MagicMock()
    manage_plugins.register(fake_app)

    print(dir(manage_plugins))

    assert fake_app.mock_calls == [
        call.register_plugin(
            name='manage-plugins',
            plugin=manage_plugins.execute,
            helptext='For managing plugins for use by forge.'
        )
    ]


@patch(f'{MODULE_PATH}.manage_plugins.ConfigHandler')
@patch(f'{MODULE_PATH}.manage_plugins.ManagePlugins')
@patch(f'{MODULE_PATH}.manage_plugins.PluginPuller')
def test_execute(mock_plugin_puller, mock_manage_plugins, mock_config):
    manage_plugins.execute([''])

    assert mock_config.mock_calls == [
        call(home_dir_path=manage_plugins.CONF_HOME,
             file_path_dir=manage_plugins.CONFIG_FILE_PATH)
    ]
    assert mock_manage_plugins.mock_calls == [
        call(plugin_puller=mock_plugin_puller(),
             config_handler=mock_config()), call().execute(args=[''])
    ]
