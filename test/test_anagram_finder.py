from .. import anagram_finder
import pytest


@pytest.fixture()
def anagramFinder():
    """Generic setup of an `AnagramFinder` instance."""
    return anagram_finder.AnagramFinder()


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
