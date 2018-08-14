from anagram_finder.utils.base_logging import BaseLogging
import pytest
import subprocess
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


@pytest.fixture(params=[
    ("test/data/example1.txt", b"no anagrams found\n"),
    ("test/data/example2.txt", b"ate eat tea\n"),
    ("test/data/example3.txt", b"do od\ndoor odor\nno on\n"),
    ("test/data/example4.txt", b"post pots spot stop\n"),
    ("test/data/example5.txt", b"no on\npost pots spot stop\nate eat tea\n")
])
def anagram_examples_stdout(request):
    return request.param


class TestMain(object):
    """Integration test for the `main.py` entrypoint."""

    def test_main_missing_args(self):
        """Verifies that `main.py` with no args returns usage."""
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py"],
            cwd="../anagram_finder/",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert b'' == cmd.stdout.read()
        assert b'Error: Missing argument "filename"' in cmd.stderr.read()
        assert 0 != cmd.wait()

    def test_main_example(self, anagram_examples_stdout):
        """Verifies expected stdout output of anagramsfrom each example file.
        """
        filepath, exp = anagram_examples_stdout
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py", filepath],
            cwd="../anagram_finder/",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert exp == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()
