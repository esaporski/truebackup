import pathlib
import pytest
from truebackup.main import compress, is_valid_path


class TestIsValidPath:
    # Test paths
    @pytest.mark.parametrize(
        'dir, expected', [
            ('.', True),
            ('..', True),
            ('/tmp', True),
            (pathlib.Path('/tmp'), True),
            ('/invalid/path', False),
            ('/root', False),
            ('/etc/hostname', False),
            ('\tmp', False),
            (pathlib.Path('/invalid/path'), False)
        ]
    )
    def test_is_valid_path(self, dir, expected):
        assert is_valid_path(dir) is expected

    # Test unsupported argument types
    @pytest.mark.parametrize(
        'dir', [
            (1),
            (None)
        ]
    )
    def test_is_valid_path_error(self, dir):
        with pytest.raises(TypeError):
            is_valid_path(dir)


@pytest.mark.usefixtures('truenas_environment')
class TestCompress:
    # Pass
    def test_pass(self):
        assert compress(
            pathlib.Path('compress.tar'), [
                pathlib.Path('data/freenas-v1.db'),
                pathlib.Path('data/geli'),
                pathlib.Path('data/pwenc_secret')
            ]
        ) is None

    # Fail - FileNotFoundError
    def test_file_not_found_error(self):
        with pytest.raises(SystemExit):  # TODO: should be FileNotFoundError
            compress(
                pathlib.Path('invalid/path/compress.tar'), [
                    pathlib.Path('data/freenas-v1.db'),
                    pathlib.Path('data/geli'),
                    pathlib.Path('data/pwenc_secret')
                ]
            )

    # Fail - tarfile.TarError
    def test_tar_error(self):
        with pytest.raises(SystemExit):  # TODO: should be tarfile.TarError
            compress(
                pathlib.Path('compress.tar'), [
                    pathlib.Path('data/notafile-v1.db'),
                    pathlib.Path('data/notafolder'),
                    pathlib.Path('data/not_a_secret')
                ]
            )

    # Fail - complete
    def test_fail(self):
        with pytest.raises(SystemExit):
            compress(
                pathlib.Path('invalid/path/compress.tar'), [
                    pathlib.Path('data/notafile-v1.db'),
                    pathlib.Path('data/notafolder'),
                    pathlib.Path('data/not_a_secret')
                ]
            )
