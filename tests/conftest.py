from mock import mock_open

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
