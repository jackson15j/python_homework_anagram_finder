from anagram_finder.dictionaries.en_us_webster import EnUsWebster
from anagram_finder.utils.filters import filter_anagram_lists
from anagram_finder.utils.filters import filter_source_str

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

    def get_anagram_lists(self, contents):
        """Return a list of sorted anagrams without any duplicates.

        @param str contents: String from a `file.read()` call.
        @returns: list of anagram tuples.
        """
        filtered_words = filter_source_str(contents)

        anagram_list = []
        for word in filtered_words:
            anagrams = self.anagram_lang_dict.get_anagrams(word)
            if anagrams:
                anagram_list.append(anagrams)

        if not anagram_list:
            return [("no anagrams found", )]

        # Filter out duplicate anagrams.
        filtered_anagram_list = filter_anagram_lists(anagram_list)
        return filtered_anagram_list
