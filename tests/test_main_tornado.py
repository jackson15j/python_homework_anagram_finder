from base_main import is_server_alive
from base_main import BaseMain
# Unused imports due to bad fixture levels.
from base_main import anagram_examples_source_file_dictionary
from base_main import anagram_examples_en_us_webster_dictionary
import anagram_finder

from os import path
from time import sleep
import pytest
import subprocess

base_module_path = path.dirname(anagram_finder.__file__)


@pytest.fixture(scope='class')
def anagramFinderProcessTornado(request):
    """Spin up the AnagramFinder process."""
    cmd_backend = subprocess.Popen(
        ["pipenv", "run", "python", "main_tornado.py"],
        cwd=base_module_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    while not is_server_alive():
        sleep(0.1)

    yield

    cmd_backend.terminate()


@pytest.mark.usefixtures('anagramFinderProcessTornado')
class TestMainTornado(BaseMain):
    pass
