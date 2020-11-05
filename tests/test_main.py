import pytest
from truebackup.main import is_valid_path


@pytest.mark.parametrize(
    'dir, expected', [
        ('.', True),
        ('..', True),
        ('/tmp', True),
        ('/invalid/path', False),
        ('/root', False),
        ('/etc/hostname', False),
        ('\tmp', False)
    ]
)
def test_is_valid_path(dir, expected):
    assert is_valid_path(dir) == expected


@pytest.mark.parametrize(
    'dir', [
        (1),
        (None)
    ]
)
def test_is_valid_path_error(dir):
    with pytest.raises(TypeError):
        is_valid_path(dir)
