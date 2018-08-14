from anagram_finder.utils.base_logging import BaseLogging
import subprocess
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


class TestMain(object):
    """Integration test for the `main.py` entrypoint."""

    def test_main_missing_args(self):
        """Verifies that `main.py` with no args returns usage."""
        cmd = subprocess.run(
            ["pipenv", "run", "python", "../anagram_finder/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        assert b'' == cmd.stdout
        assert b'Error: Missing argument "filename"' in cmd.stderr
        assert 0 != cmd.returncode
