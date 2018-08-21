from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum
from anagram_finder.utils.base_logging import BaseLogging

import pytest
import logging

BaseLogging().default_config()
log = logging.getLogger(__name__)


@pytest.fixture()
def anagramFinder():
    """Generic setup of an `AnagramFinder` instance."""
    return AnagramFinder()


@pytest.fixture(params=[
    # source_str, exp_result.
    ("the quick brown fox", [("no anagrams found", )]),
    ("eat my tea", [("eat", "tea")]),
    ("do or door no no", [("no anagrams found", )]),
    ("pots stop pots spot stop", [("pots", "spot", "stop")]),
    ("on pots no stop eat\nate pots spot stop tea",
     [("no", "on"), ("pots", "spot", "stop"), ("ate", "eat", "tea")])
])
def anagram_examples_source_file_dictionary(request):
    return request.param


# Note: Why does the Webster dictionary not have "eat"??
# FIXME: Webster doesn't have `TOPS` as a plural of `TOP` in it's graph.json.
# Note: Apparently: 'OD', is a word in the Webster dictionary:
# > 'An alleged force or natural power, supposed, by Reichenbach andothers, to
# > produce the phenomena of mesmerism, and to be developed byvarious agencies,
# > as by magnets, heat, light, chemical or vitalaction, etc.; -- called also
# > odyle or the odylic force. [Archaic]That od force of German Reichenbach
# > Which still, from female fingertips, burnt blue. Mrs. Browning.'
# FIXME: Webster is an English US dictionary. Find an English GB dictionary so
# that I can remove the US anagram ["door", "odor"].
@pytest.fixture(params=[
    # source_str, exp_result.
    ("the quick brown fox", [("no anagrams found",)]),
    ("eat my tea", [("ate", "eat", "tea")]),
    ("do or door no no", [("do", "od"), ("door", "odor"), ("no", "on")]),
    ("pots stop pots spot stop", [("post", "pots", "spot", "stop")]),
    ("on pots no stop eat\nate pots spot stop tea",
     [("no", "on"), ("post", "pots", "spot", "stop"), ("ate", "eat", "tea")])
])
def anagram_examples_en_us_webster_dictionary(request):
    return request.param


@pytest.mark.usefixtures("anagramFinder")
class TestAnagramFinder(object):
    """Unittests for the AnagramFinder class."""

    def test_get_anagram_lists(
            self, anagramFinder, anagram_examples_en_us_webster_dictionary):
        """Positively verify `_get_anagram_lists()`."""
        log.debug(anagram_examples_en_us_webster_dictionary)
        content, exp = anagram_examples_en_us_webster_dictionary

        result = anagramFinder.get_anagram_lists(content)
        assert exp == result

    def test_get_anagram_lists_source_file_anagram_dict(
            self, anagram_examples_source_file_dictionary):
        """Positively verify `_get_anagram_lists()`."""
        log.debug(anagram_examples_source_file_dictionary)
        content, exp = anagram_examples_source_file_dictionary
        anagramFinder = AnagramFinder(AnagramLangDictEnum.SOURCE_FILE)

        result = anagramFinder.get_anagram_lists(content)
        assert exp == result
