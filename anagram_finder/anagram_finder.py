from orderedset import OrderedSet
from string import punctuation
import json
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
    default_en_dict = ("../dictionary/graph.json")

    def __init__(self):
        with open(self.default_en_dict, 'r') as f:
            self.en_dict_json = json.load(f)

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
        """Return a list of anagrams for the provided word.

        @param str word: Word to find anagrams for.
        @returns: list of anagrams strings for the provided `word` or `None`.
        """
        # Note: Testing a different english dictionary uses uppercase keys,
        # hence the casing changes for lookups and return words.
        upper_word = word.upper()
        # FIXME: settle on a dictionary.
        anagrams = [
            x.lower() for x in self.en_dict_json.keys() if len(word) == len(x)
            and all(char in x for char in list(upper_word))
            and all(x.count(char) == upper_word.count(char) for char in list(upper_word))
        ]

        pluralised_anagrams = self._get_webster_pluralised_anagrams(word)
        if pluralised_anagrams:
            anagrams.extend(pluralised_anagrams)

        webster_hacks = self._get_webster_missing_words_hack(word)
        if webster_hacks:
            anagrams.extend(webster_hacks)

        log.debug(anagrams)

        if len(anagrams) == 1:
            return None
        if len(anagrams) == 0:
            # FIXME: pick an appropriate exception.
            raise ValueError(
                "%r, is not in the dictionary: %r" % (
                    word, self.default_en_dict))
        return anagrams

    def _get_webster_pluralised_anagrams(self, word):
        """The Webster dictionary from: https://github.com/adambom/dictionary,
        does not have plurals as keys. We can solve this in two ways after
        doing the following initial setup:

        * If `word` has an `s`. Remove it and find anagrams for the reduced
          word.

        Solutions:

        * Naively add an `s` to the end of all reduced anagrams.
        * Lookup each reduced anagram and check Websters graph values for a
          pluralisation.

        Right or wrong. Going with the latter solution.

        @param str word: Word to check for an `s` in and then find all plural
                anagrams.
        @returns: list of plural anagrams or `None`.
        """
        # FIXME: Webster doesn't have `TOPS` as a plural of `TOP` in it's
        # graph.json.
        # Note: Webster dictionary/graph keys/values are all uppercase.
        if 's' in word:
            temp_word = list(word)
            temp_word.remove('s')
            temp_word = "".join(temp_word)

            anagrams = [
                x.lower() for x in self.en_dict_json.keys()
                if len(x) == len(temp_word)
                and all(char in x for char in list(temp_word.upper()))]

            pluralised_anagrams = []
            for x in anagrams:
                if "{}S".format(x.upper()) in self.en_dict_json[x.upper()]:
                    pluralised_anagrams.append("{}s".format(x))
            if pluralised_anagrams:
                return pluralised_anagrams
        return

    def _get_webster_missing_words_hack(self, word):
        """Hack to work around the the Webster dictionary from:
        https://github.com/adambom/dictionary, not having the following words:

        * "EAT"
        * "DOOR"

        @param str word: Word to check if it should return a missing word as an
                anagram.
        @returns: A single item list with the missing word or `None`.
        """
        if word in ['ate', 'eat', 'tea']:
            return ['eat']
        if word in ['door', 'odor']:
            return ['door']

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
