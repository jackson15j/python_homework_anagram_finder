from .. import anagram_finder
import pytest


@pytest.fixture()
def anagramFinder():
    """Generic setup of an `AnagramFinder` instance."""
    return anagram_finder.AnagramFinder()


@pytest.fixture(params=[
    ("the quick brown fox", {"no anagrams found", }),
    ("eat my tea", {"eat", "eat"}),
    ("do or door no no", {"no anagrams found", }),
    ("pots stop pots spot stop", {"pots", "stop", "spot"}),
    ("on pots no stop eat\nate pots spot stop tea",
     {("on", "no"), ("pots", "stop", "spot"), ("eat", "ate" "tea")})
])
def anagram_examples(request):
    return request.param


@pytest.fixture(params=[
    ("the quick brown fox", "no anagrams found"),
    ("eat my tea", "eat eat"),
    ("do or door no no", "no anagrams found"),
    ("pots stop pots spot stop", "pots stop spot"),
    ("on pots no stop eat\nate pots spot stop tea",
     "on no\npots stop spot\neat ate tea")
])
def anagram_examples_stdout(request):
    # TODO: move to the integration test when I need to check my stdout
    # printer.
    return request.param


@pytest.mark.usefixtures("anagramFinder")
class TestAnagramFinder(object):
    """Unittests for the AnagramFinder class."""

    def test_filter_source(self, anagramFinder):
        """Positively verify `_filter_source()`."""
        a = "a fake source with punctuation. And new\nlines\ninside it. fake."
        exp = {
            "a", "fake", "source", "with", "punctuation", "and", "new",
            "lines", "inside", "it"}

        result = anagramFinder._filter_source(a)
        assert exp == result

    def test_filter_anagram_lists(self, anagramFinder):
        """Positively verify `_filter_anagram_lists()`."""
        a = ['a', 'b', 'c']
        b = ['b', 'c', 'a']
        c = ['d', 'e']
        d = [a, a, b, b, c, c]
        exp = {tuple(a), tuple(c)}

        result = anagramFinder._filter_anagram_lists(d)
        assert exp == result

    def test_get_anagrams(self, anagramFinder):
        """Positively verify `_get_anagrams()`."""
        a = "stop"
        exp = ["stop", "pots", "tops"]

        result = anagramFinder._get_anagrams(a)
        # instead of doing something like:
        # `assert bool(x in exp for x in result)` or asserts within the for
        # loop, I'm sorting the lists to maintain debug output.
        exp.sort()
        result.sort()
        assert exp == result

    def test_get_anagram_lists(self, anagramFinder, anagram_examples):
        """Positively verify `_get_anagram_lists()`."""
        content, exp = anagram_examples

        result = anagramFinder.get_anagram_lists(content)
        assert exp == result
