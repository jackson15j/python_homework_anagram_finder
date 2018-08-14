from .. import anagram_finder
import pytest


@pytest.fixture()
def anagramFinder():
    """Generic setup of an `AnagramFinder` instance."""
    return anagram_finder.AnagramFinder()


# FIXME: the example provided is not correct in all cases. eg.
# * "eat my tea" should return: "eat ate tea" instead of "eat tea".
# * "do or door no no" should return: "no on" instead of "no anagrams found"
@pytest.fixture(params=[
    ("the quick brown fox", {("no anagrams found")}),
    ("eat my tea", {("eat", "tea")}),
    ("do or door no no", {("no anagrams found")}),
    ("pots stop pots spot stop", {("pots", "stop", "spot")}),
    ("on pots no stop eat\nate pots spot stop tea",
     {("on", "no"), ("pots", "stop", "spot"), ("eat", "ate" "tea")})
])
def anagram_examples(request):
    return request.param


# FIXME: Why does the Webster dictionary not have "eat"??
@pytest.fixture(params=[
    ("the quick brown fox", {("no anagrams found")}),
    ("eat my tea", {("ate", "eat", "tea")}),
    ("do or door no no", {("on", "no")}),
    ("pots stop pots spot stop", {("post", "pots", "spot", "stop")}),
    ("on pots no stop eat\nate pots spot stop tea",
     {("on", "no"), ("post", "pots", "spot", "stop"), ("ate", "eat", "tea")})
])
def anagram_examples_fixed(request):
    return request.param


# FIXME: the example provided is not correct in all cases. eg.
@pytest.fixture(params=[
    ("the quick brown fox", "no anagrams found"),
    ("eat my tea", "eat tea"),
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
        # FIXME: https://github.com/adambom/dictionary, doesn't have pluralised
        # words as keys. These can be found in the value list of
        # `graph.json`. Might have to do something crazy like "if word contains
        # `s`, do a look up of `len(word) -1` and filter for words based of
        # remaining characters **and** `s` is the final character.
        exp = ["stop", "pots", "tops", "post"]

        result = anagramFinder._get_anagrams(a)
        # instead of doing something like:
        # `assert bool(x in exp for x in result)` or asserts within the for
        # loop, I'm sorting the lists to maintain debug output.
        exp.sort()
        result.sort()
        assert exp == result

    def test_get_anagrams_returns_none(self, anagramFinder):
        """Verify `_get_anagrams()` returns None if no anagrams are found."""
        a = "fox"
        exp = None

        result = anagramFinder._get_anagrams(a)
        assert exp == result

    def test_get_anagram_lists(self, anagramFinder, anagram_examples_fixed):
        """Positively verify `_get_anagram_lists()`."""
        print(anagram_examples_fixed)
        content, exp = anagram_examples_fixed

        result = anagramFinder.get_anagram_lists(content)
        assert exp == result
