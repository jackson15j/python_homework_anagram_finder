from anagram_finder.dictionaries.source_file import SourceFile
from anagram_finder.utils.base_logging import BaseLogging
import pytest
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


@pytest.fixture()
def anagram_dict():
    """Generic setup of an `SourceFile()` instance."""
    return SourceFile()


# FIXME: the example provided is not correct in all cases. eg.
# * "eat my tea" should return: "eat ate tea" instead of "eat tea".
# * "do or door no no" should return: "no on" instead of "no anagrams found"
@pytest.fixture(params=[
    ("fox", "the quick brown fox", None),
    ("eat", "eat my tea", ["eat", "tea"]),
    ("no", "do or door no no", None),
    ("pots", "pots stop pots spot stop", ["pots", "stop", "spot"]),
    ("on", "on pots no stop eat\nate pots spot stop tea", ["on", "no"]),
    ("pots", "on pots no stop eat\nate pots spot stop tea", ["pots", "stop", "spot"]),
    ("eat", "on pots no stop eat\nate pots spot stop tea", ["eat", "ate", "tea"])
])
def anagram_examples(request):
    return request.param


@pytest.mark.usefixtures("anagram_dict")
class TestSourceFile(object):
    """Unittests for the SourceFile dictionary class."""

    def test_get_anagrams(self, anagram_dict, anagram_examples):
        """Positively verify `get_anagrams()`."""
        log.debug(anagram_examples)
        word, content, exp = anagram_examples

        result = anagram_dict.get_anagrams(word, content)
        if exp:
            exp.sort()
        if result:
            result.sort()
        assert exp == result
