import pytest
from mock import mock_open, patch

# Credit to: https://gist.github.com/adammartinez271828/137ae25d0b817da2509c1a96ba37fc56


def multi_mock_open(*file_contents):
    """Create a mock "open" that will mock open multiple files in sequence
    Args:
        *file_contents ([str]): a list of file contents to be returned by open
    Returns:
        (MagicMock) a mock opener that will return the contents of the first
            file when opened the first time, the second file when opened the
            second time, etc.
    """
    mock_files = [mock_open(read_data=content).return_value for content in file_contents]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    return mock_opener


@pytest.fixture()
def mock_echo():
    with patch('click.echo') as mock:
        yield mock


@pytest.fixture()
def mock_listdir():
    with patch('os.listdir') as mock:
        yield mock


@pytest.fixture()
def mock_tabulate():
    with patch('tabulate.tabulate') as mock:
        yield mock


@pytest.fixture()
def mock_popen():
    with patch('subprocess.Popen') as mock:
        yield mock


@pytest.fixture()
def mock_spinner():
    with patch('halo.Halo') as mock:
        yield mock
