"""Allow truebackup to be executable through `python -m truebackup`."""
from truebackup.cli import main


if __name__ == '__main__':  # pragma: no cover
    main(prog_name='truebackup')
