from anagram_finder.utils.base_logging import BaseLogging
import subprocess
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


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

    def test_main_example(self):
        """"""
        cmd = subprocess.Popen(
            ["pipenv", "run", "python", "main.py", "test/data/example1.txt"],
            cwd="../anagram_finder/",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert b'no anagrams found\n' == cmd.stdout.read()
        assert b'' == cmd.stderr.read()
        assert 0 == cmd.wait()
