import unittest
from .manage_plugins import ManagePlugins
from .test_stubs.stub_plugin_puller import StubPluginPuller
from .test_stubs.stub_config_parser import StubPluginConfigHandler
from .test_stubs.stub_plugin_puller import StubPluginPullerWithError


class ManagePluginsLogicTest(unittest.TestCase):

    def test_add_with_no_url_error(self):
        with self.assertRaises(SystemExit) as raised_ex:
            ManagePlugins(StubPluginPuller(), StubPluginConfigHandler()).execute(['-a'])
        self.assertEqual(raised_ex.exception.code, 1)

    def test_add_all_works(self):
        try:
            unit_under_test = ManagePlugins(StubPluginPuller(), StubPluginConfigHandler())
            args = ['-a', '-p some_url/forge-someplugin']
            unit_under_test.execute(args)
        except SystemExit as ex:
            self.fail(ex)

    def test_add_fails_name_format(self):
        with self.assertRaises(SystemExit) as raised_ex:
            unit_under_test = ManagePlugins(StubPluginPuller(), StubPluginConfigHandler())
            args = ['-a', '-p some_url/someplugin']
            unit_under_test.execute(args)

        self.assertEqual(raised_ex.exception.code, 1)

    def test_update_without_name(self):
        try:
            unit_under_test = ManagePlugins(StubPluginPuller(), StubPluginConfigHandler())
            args = ['-u']
            unit_under_test.execute(args)
        except SystemExit as ex:
            self.fail(ex)

    def test_update_without_name_fails_due_to_command_error(self):
        with self.assertRaises(SystemExit) as raised_ex:
            unit_under_test = ManagePlugins(StubPluginPullerWithError(), StubPluginConfigHandler())
            args = ['-u']
            unit_under_test.execute(args)

        self.assertEqual(raised_ex.exception.code, 1)

    def test_update_with_name(self):
        try:
            unit_under_test = ManagePlugins(StubPluginPuller(), StubPluginConfigHandler())
            args = ['-u', '-n some_name']
            unit_under_test.execute(args)
        except SystemExit as ex:
            self.fail(ex)

    def test_update_with_name_fails(self):
        with self.assertRaises(SystemExit) as raised_ex:
            unit_under_test = ManagePlugins(StubPluginPullerWithError(), StubPluginConfigHandler())
            args = ['-u', '-n some_bad_name']
            unit_under_test.execute(args)

        self.assertEqual(raised_ex.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
