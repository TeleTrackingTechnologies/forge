import forge
import pytest
from forge.exceptions import (PluginManagementFatalException,
                              PluginManagementWarnException)
from mock import patch


@patch('forge.forge_cli')
def test_main_fatal_exception(mock_cli):

    mock_cli.side_effect = PluginManagementFatalException('some fatal message')

    with pytest.raises(SystemExit) as err:
        forge.main()

    mock_cli.assert_called_once()
    assert str(err.value) == '1'


@patch('forge.forge_cli')
def test_main_warning_exception(mock_cli):

    mock_cli.side_effect = PluginManagementWarnException('some fatal message')

    with pytest.raises(SystemExit) as err:
        forge.main()

    mock_cli.assert_called_once()
    assert str(err.value) == '0'
