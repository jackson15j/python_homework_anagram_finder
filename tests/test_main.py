from anagram_finder.utils.base_logging import BaseLogging
import anagram_finder

from os import path
from time import sleep
import pytest
import subprocess
import logging
import requests

BaseLogging().default_config()
log = logging.getLogger(__name__)
base_module_path = path.dirname(anagram_finder.__file__)
data_path = path.join(base_module_path, "../tests/data/")


@pytest.fixture(params=[
    (path.join(data_path, "example1.txt"), b"no anagrams found\n"),
    (path.join(data_path, "example2.txt"), b"ate eat tea\n"),
    (path.join(data_path, "example3.txt"), b"do od\ndoor odor\nno on\n"),
    (path.join(data_path, "example4.txt"), b"post pots spot stop\n"),
    (path.join(data_path, "example5.txt"), b"no on\npost pots spot stop\nate eat tea\n")
])
def anagram_examples_stdout_en_us_webster_dictionary(request):
    return request.param


@pytest.fixture(params=[
    (path.join(data_path, "example1.txt"), b"no anagrams found\n"),
    (path.join(data_path, "example2.txt"), b"eat tea\n"),
    (path.join(data_path, "example3.txt"), b"no anagrams found\n"),
    (path.join(data_path, "example4.txt"), b"pots spot stop\n"),
    (path.join(data_path, "example5.txt"), b"no on\npots spot stop\nate eat tea\n")
])
def anagram_examples_stdout_source_file_dictionary(request):
    return request.param


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


def is_server_alive():
    """Poll check to verify the backed AnagramFinder service is running."""
    try:
        response = requests.get("http://127.0.0.1:5000/")
    except requests.ConnectionError:
        return False
    return response.status_code is 200


@pytest.mark.usefixtures('anagramFinderProcess')
class TestMain(object):
    """Integration test for the `main.py` entrypoint."""

    client_path = path.join(base_module_path, "client")

    def test_main_missing_args(self):
        """Verifies that `main.py` with no args returns usage."""
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "cli.py"],
            cwd=self.client_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert b'' == cmd.stdout.read()
        assert b'Error: Missing argument "filename"' in cmd.stderr.read()
        assert 0 != cmd.wait()

    def test_main_example_default_anagram_dict(
            self,
            anagram_examples_stdout_en_us_webster_dictionary):
        """Verifies expected stdout output of anagrams from each example file
        against the default anagram dictionary.
        """
        filepath, exp = anagram_examples_stdout_en_us_webster_dictionary
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "cli.py", filepath],
            cwd=self.client_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()

    def test_main_example_en_us_webster_anagram_dict(
            self,
            anagram_examples_stdout_en_us_webster_dictionary):
        """Verifies expected stdout output of anagrams from each example file
        against the EN US Webster anagram dictionary.
        """
        filepath, exp = anagram_examples_stdout_en_us_webster_dictionary
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "cli.py",
             "--dictionary=en-us-webster", filepath],
            cwd=self.client_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()

    def test_main_example_source_file_anagram_dict(
            self,
            anagram_examples_stdout_source_file_dictionary):
        """Verifies expected stdout output of anagrams from each example file
        against the source file as the anagram dictionary.
        """
        filepath, exp = anagram_examples_stdout_source_file_dictionary
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "cli.py", "--dictionary=source-file",
             filepath],
            cwd=self.client_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()
