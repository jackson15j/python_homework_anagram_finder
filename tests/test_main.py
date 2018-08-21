from anagram_finder.utils.base_logging import BaseLogging
import anagram_finder

from os import path
import pytest
import subprocess
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


@pytest.fixture(params=[
    ("../tests/data/example1.txt", b"no anagrams found\n"),
    ("../tests/data/example2.txt", b"ate eat tea\n"),
    ("../tests/data/example3.txt", b"do od\ndoor odor\nno on\n"),
    ("../tests/data/example4.txt", b"post pots spot stop\n"),
    ("../tests/data/example5.txt", b"no on\npost pots spot stop\nate eat tea\n")
])
def anagram_examples_stdout_en_us_webster_dictionary(request):
    return request.param


@pytest.fixture(params=[
    ("../tests/data/example1.txt", b"no anagrams found\n"),
    ("../tests/data/example2.txt", b"eat tea\n"),
    ("../tests/data/example3.txt", b"no anagrams found\n"),
    ("../tests/data/example4.txt", b"pots spot stop\n"),
    ("../tests/data/example5.txt", b"no on\npots spot stop\nate eat tea\n")
])
def anagram_examples_stdout_source_file_dictionary(request):
    return request.param


class TestMain(object):
    """Integration test for the `main.py` entrypoint."""

    base_module_path = path.dirname(anagram_finder.__file__)

    def test_main_missing_args(self):
        """Verifies that `main.py` with no args returns usage."""
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py"],
            cwd=self.base_module_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert b'' == cmd.stdout.read()
        assert b'Error: Missing argument "filename"' in cmd.stderr.read()
        assert 0 != cmd.wait()

    def test_main_example_default_anagram_dict(
            self, anagram_examples_stdout_en_us_webster_dictionary):
        """Verifies expected stdout output of anagrams from each example file
        against the default anagram dictionary.
        """
        filepath, exp = anagram_examples_stdout_en_us_webster_dictionary
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py", filepath],
            cwd=self.base_module_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()

    def test_main_example_en_us_webster_anagram_dict(
            self, anagram_examples_stdout_en_us_webster_dictionary):
        """Verifies expected stdout output of anagrams from each example file
        against the EN US Webster anagram dictionary.
        """
        filepath, exp = anagram_examples_stdout_en_us_webster_dictionary
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py",
             "--dictionary=en-us-webster", filepath],
            cwd=self.base_module_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()

    def test_main_example_source_file_anagram_dict(
            self, anagram_examples_stdout_source_file_dictionary):
        """Verifies expected stdout output of anagrams from each example file
        against the source file as the anagram dictionary.
        """
        filepath, exp = anagram_examples_stdout_source_file_dictionary
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py", "--dictionary=source-file",
             filepath],
            cwd=self.base_module_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()
