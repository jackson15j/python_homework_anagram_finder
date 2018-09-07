from base_main import is_server_alive
from base_main import BaseMain
import anagram_finder

from os import path
from time import sleep
import pytest
import subprocess

base_module_path = path.dirname(anagram_finder.__file__)


@pytest.fixture(scope='class')
def anagramFinderProcess(request):
    """Spin up the AnagramFinder process."""
    cmd_backend = subprocess.Popen(
        ["pipenv", "run", "python", "main.py"],
        cwd=base_module_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    while not is_server_alive():
        sleep(0.1)

    yield

    cmd_backend.terminate()


@pytest.mark.usefixtures('anagramFinderProcess')
class TestMain(BaseMain):
    pass
