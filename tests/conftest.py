import os
import pathlib
import pytest
import shutil


@pytest.fixture()
def truenas_environment(tmpdir):
    # Create '/etc', '/data' and '/data/geli' directories
    etc = tmpdir.mkdir('etc')
    data = tmpdir.mkdir('data')
    geli = data.mkdir('geli')

    # Create '/etc/version' file
    version = etc.join('version')
    version.write('FakeNAS-66.6-RELEASE (p314159265)')

    # Create '/data/freenas-v1.db' file
    db = data.join('freenas-v1.db')
    db.write('fakenas')

    # Create '/data/geli/*.key' file
    key = geli.join('fake666ca86c9a1c460a17322666fake.key')
    key.write('fakekey')

    # Create '/data/pwenc_secret' file
    secret = data.join('pwenc_secret')
    secret.write('fakesecret')

    old_cwd = pathlib.Path.cwd()
    os.chdir(tmpdir)

    yield
    os.chdir(old_cwd)
    shutil.rmtree(tmpdir)
