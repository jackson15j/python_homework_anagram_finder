from anagram_finder.dictionaries.ianagram_lang_dict import IAnagramLangDict

from os import path
import json
import logging

log = logging.getLogger(__name__)


class EnUsWebster(IAnagramLangDict):
    """
    Anagram finding class centred on the US English Webster dictionary from:
    https://github.com/adambom/dictionary, as a git submodule for offline
    lookups.
    """
    dict_path = ("en_us_webster/graph.json")
    dict_full_path = path.join(path.dirname(__file__), dict_path)

    def __init__(self):
        with open(self.dict_full_path, 'r') as f:
            self.en_dict_json = json.load(f)

    def get_anagrams(self, word, source_str=None):
        """Return a list of anagrams for the provided word.

        @param str word: Word to find anagrams for.
        @param str source_str: Unused.
        @returns: list of anagrams strings for the provided `word` or `None`.
        """
        # Note: Testing a different english dictionary uses uppercase keys,
        # hence the casing changes for lookups and return words.
        upper_word = word.upper()
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
