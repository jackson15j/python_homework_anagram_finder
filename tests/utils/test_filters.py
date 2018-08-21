from anagram_finder.utils.filters import filter_anagram_lists
from anagram_finder.utils.filters import filter_source_str


class TestFilters(object):
    """Unittests for the Filters class."""
    def test_filter_source(self):
        """Positively verify `_filter_source()`."""
        a = "a fake source with punctuation. And new\nlines\ninside it. fake."
        exp = [
            "a", "fake", "source", "with", "punctuation", "and", "new",
            "lines", "inside", "it"]

        result = filter_source_str(a)
        assert exp == result

    def test_filter_anagram_lists(self):
        """Positively verify `_filter_anagram_lists()`."""
        a = ['a', 'b', 'c']
        b = ['b', 'c', 'a']
        c = ['d', 'e']
        d = [a, a, b, b, c, c]
        exp = [tuple(a), tuple(c)]

        result = filter_anagram_lists(d)
        assert exp == result
