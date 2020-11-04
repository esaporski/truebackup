#!/usr/bin/env python
import pathlib
from setuptools import setup


def read(rel_path):
    here = pathlib.Path(__file__).parent.absolute()
    with here.joinpath(rel_path).open('r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError('Unable to find version string.')


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'click>=7.1.2'
]

setup(
    name='truebackup',
    version=get_version('truebackup/main.py'),
    description=(
        'A command-line utility that can help you perform '
        'automated system configuration backups for TrueNAS.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Eduardo Saporski',
    author_email='esaporski@protonmail.com',
    url='https://github.com/esaporski/truebackup',
    packages=['truebackup'],
    package_dir={'truebackup': 'truebackup'},
    entry_points={
        'console_scripts': [
            'truebackup=truebackup.main:main'
        ]
    },
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requirements,
    license='GPLv3',
)
