import pathlib
import pytest
from click.testing import CliRunner
from truebackup.__main__ import main


@pytest.fixture(scope='session')
def cli_runner():
    """Fixture that returns a helper function to run the truebackup cli."""
    runner = CliRunner()

    def cli_main(*cli_args, **cli_kwargs):
        """Run truebackup cli main with the given args."""
        return runner.invoke(main, cli_args, **cli_kwargs)

    return cli_main


@pytest.mark.usefixtures('truenas_environment')
class TestMain:
    def test_secret_seed(self, cli_runner):
        response = cli_runner(f'--output-dir {pathlib.Path.cwd()}')
        print(response.stdout)
        assert response.exit_code == 0

    # def test_pool_keys(self):
    #     assert main(
    #         '.',    # output_dir
    #         False,  # secret_seed
    #         True    # pool_keys
    #     ) is None

    # def test_all(self):
    #     assert main(
    #         '.',    # output_dir
    #         True,   # secret_seed
    #         True    # pool_keys
    #     ) is None

    # def test_db_only(self):
    #     assert main(
    #         '.',    # output_dir
    #         False,  # secret_seed
    #         False   # pool_keys
    #     ) is None
