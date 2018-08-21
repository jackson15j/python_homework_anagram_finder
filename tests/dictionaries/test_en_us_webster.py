from anagram_finder.dictionaries.en_us_webster import EnUsWebster
from anagram_finder.utils.base_logging import BaseLogging
import pytest
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


@pytest.fixture()
def anagram_dict():
    """Generic setup of an `EnUsWebster()` instance."""
    return EnUsWebster()


@pytest.mark.usefixtures("anagram_dict")
class TestEnUsWebster(object):
    """Unittests for the EnUsWebster dictionary class."""

    def test_get_anagrams(self, anagram_dict):
        """Positively verify `_get_anagrams()`."""
        a = "stop"
        exp = ["stop", "pots", "spot", "post"]

        result = anagram_dict.get_anagrams(a)
        # instead of doing something like:
        # `assert bool(x in exp for x in result)` or asserts within the for
        # loop, I'm sorting the lists to maintain debug output.
        exp.sort()
        result.sort()
        assert exp == result

    def test_get_anagrams_returns_none(self, anagram_dict):
        """Verify `_get_anagrams()` returns None if no anagrams are found."""
        a = "fox"
        exp = None

        result = anagram_dict.get_anagrams(a)
        assert exp == result
