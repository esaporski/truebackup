import click
import datetime
import os
import pathlib
import shutil
import subprocess
import sys
import tarfile


__version__ = '0.0.1'


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


def compress(file_path, members):
    try:
        # Open for uncompressed writing.
        with tarfile.open(file_path, mode='w') as tar:
            for member in members:
                tar.add(member, arcname=member.name)
    except (FileNotFoundError, tarfile.TarError) as error:
        sys.exit(error)


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
    if not is_valid_path(output_dir):
        sys.exit(f'[Error] "{output_dir}" is not a valid path')

    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Get hostname
    try:
        result = subprocess.run(['hostname', '-s'], capture_output=True, text=True)
        result.check_returncode()
        hostname = result.stdout.strip()
    except subprocess.CalledProcessError as error:
        sys.exit(f'{error}\n\t{error.stderr}')
    except FileNotFoundError as error:
        sys.exit(error)

    # Get TrueNAS version string
    version_path = pathlib.Path('/etc/version')

    try:
        with version_path.open('r') as version:
            version = version.read().split(' ')[0].strip()
    except FileNotFoundError as error:
        sys.exit(error)

    # Backup file path
    file_path = f'{output_dir}/{hostname}-{version}-{now}'

    if secret_seed or pool_keys:
        # TODO: pathlib.Path('foo_path').append_suffix('.bar')
        file_path += '.tar'

        compress(file_path, [
            pathlib.Path('/data/freenas-v1.db'),
            pathlib.Path('/data/geli'),
            pathlib.Path('/data/pwenc_secret')
        ])
    else:
        # TODO: pathlib.Path('foo_path').append_suffix('.bar')
        file_path += '.db'

        try:
            shutil.copy2('/data/freenas-v1.db', file_path)
        except (FileNotFoundError, shutil.Error) as error:
            sys.exit(error)


if __name__ == '__main__':
    main()
