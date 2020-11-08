"""Main `truebackup` CLI."""
import click
import os
import pathlib
import sys
from truebackup import __version__
from truebackup.main import truebackup


def version_msg():
    python_version = sys.version[:3]
    location = (pathlib.Path(__file__).parent).parent.absolute()
    message = f'{__version__} from {location} (Python {python_version})'
    return message


def is_valid_path(dir):
    dir = pathlib.Path(dir)

    if not (dir.exists() and
            dir.is_dir() and
            os.access(dir, os.W_OK)):
        return False
    else:
        return True


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-V', '--version', message=version_msg())
@click.option(
    '-o',
    '--output-dir',
    type=click.Path(),
    required=True,
    help='File output location (eg., \'/tmp/backup\').'
)
@click.option(
    '--secret-seed',
    is_flag=True,
    help='Export password secret seed.',
)
@click.option(
    '--pool-keys',
    is_flag=True,
    help='Export pool encryption keys.',
)
def main(output_dir, secret_seed, pool_keys):
    output_dir = pathlib.Path(output_dir)

    if not (output_dir.exists() and
            output_dir.is_dir() and
            os.access(output_dir, os.W_OK)):
        click.echo(f'[Error] "{output_dir}" is not a valid path')
        sys.exit(1)

    try:
        truebackup(
            output_dir,
            secret_seed,
            pool_keys
        )
    except Exception as error:
        click.echo(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
