import forge
import pytest
from forge.exceptions import (PluginManagementFatalException,
                              PluginManagementWarnException)
from mock import patch


@pytest.fixture()
def mock_inject():
    with patch('forge.inject_forge_plugins') as mock:
        yield mock


@pytest.fixture()
def mock_cli():
    with patch('forge.forge_cli') as mock:
        yield mock


def test_main_fatal_exception(mock_cli, mock_inject):

    mock_cli.side_effect = PluginManagementFatalException('some fatal message')

    with pytest.raises(SystemExit) as err:
        forge.main()

    mock_cli.assert_called_once()
    mock_inject.assert_called_once()
    assert str(err.value) == '1'


def test_main_warning_exception(mock_cli, mock_inject):

    mock_cli.side_effect = PluginManagementWarnException('some fatal message')

    with pytest.raises(SystemExit) as err:
        forge.main()

    mock_cli.assert_called_once()
    mock_inject.assert_called_once()
    assert str(err.value) == '0'
