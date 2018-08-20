from dictionaries.en_us_webster import EnUsWebster

from orderedset import OrderedSet
from string import punctuation
import logging

log = logging.getLogger(__name__)


class AnagramFinder(object):
    """
    Anagram Finder class that finds anagrams of the words passed in as a source
    string.
    """
    # Using: an American English Webster dictionary from:
    # https://github.com/adambom/dictionary, as a git submodule for offline
    # lookups.
    #
    # FIXME: A quick google doesn't show any GB english dictionaries in JSON
    # format. May have to install a platform dictionary (eg. Aspell, Hunspell)
    # or add a restclient/web scraper to get from an online resource.
    #
    # Note: Had previously used: https://github.com/dwyl/english-words/, but
    # removed it due to too many words that would not be considered standard.
    # Note: This Webster dictionary's keys/values are upper case.

    def __init__(self):
        # FIXME: Allow Client to define the dictionary.
        self.anagram_lang_dict = EnUsWebster()

    def _filter_anagram_lists(self, anagram_list):
        """Sorts and filters the nested anagram list to remove duplicates.

        @param list anagram_list: Nested list of unsorted anagram lists.
        @returns: `set()` of anagram lists.
        """
        # Sort each sub-anagram list, then tuple, so that I can do an
        # OrderedSet on them (OrderedSet since a requirement is to return
        # anagrams in file read order).
        [x.sort() for x in anagram_list]
        ret_val = [tuple(x) for x in anagram_list]
        ret_val = list(OrderedSet(ret_val))
        return ret_val

    def _filter_source(self, contents):
        """Filter the source content to remove punctuation and duplicate words.

        @param str contents: String from a `file.read()` call.
        @returns: `set()`.
        """
        # Downcase to remove duplicates due to capitalisation.
        ret_val = contents.lower()
        # Remove punctuation from the string.
        translator = str.maketrans('', '', punctuation)
        ret_val = ret_val.translate(translator)
        ret_val = OrderedSet(ret_val.split())
        return list(ret_val)

    def _get_anagrams(self, word):
        # FIXME: half-step refactor, whilst I'm pushing functionality out to a
        # new class. Need to fix unittests before I can remove this function.
        return self.anagram_lang_dict.get_anagrams(word)

    def get_anagram_lists(self, contents):
        """Return a list of sorted anagrams without any duplicates.

        @param str contents: String from a `file.read()` call.
        @returns: list of anagram tuples.
        """
        filtered_words = self._filter_source(contents)

        anagram_list = []
        for word in filtered_words:
            anagrams = self._get_anagrams(word)
            if anagrams:
                anagram_list.append(anagrams)

        if not anagram_list:
            return [("no anagrams found", )]

        # Filter out duplicate anagrams.
        filtered_anagram_list = self._filter_anagram_lists(anagram_list)
        return filtered_anagram_list
