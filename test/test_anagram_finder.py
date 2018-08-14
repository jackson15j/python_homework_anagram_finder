from .. import anagram_finder


class TestAnagramFinder(object):
    def test_filter_source(self):
        a = "a fake source with punctuation. And new\nlines\ninside it. fake."
        exp = {
            "a", "fake", "source", "with", "punctuation", "and", "new",
            "lines", "inside", "it"}

        anagramFinder = anagram_finder.AnagramFinder()
        result = anagramFinder._filter_source(a)
        assert exp == result

    def test_filter_anagram_lists(self):
        a = ['a', 'b', 'c']
        b = ['b', 'c', 'a']
        c = ['d', 'e']
        d = [a, a, b, b, c, c]
        exp = {tuple(a), tuple(c)}

        anagramFinder = anagram_finder.AnagramFinder()
        result = anagramFinder._filter_anagram_lists(d)
        assert exp == result
