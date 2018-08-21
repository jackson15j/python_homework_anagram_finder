from anagram_finder.dictionaries.en_us_webster import EnUsWebster
from anagram_finder.dictionaries.source_file import SourceFile
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum
from anagram_finder.utils.filters import filter_anagram_lists
from anagram_finder.utils.filters import filter_source_str

import logging

log = logging.getLogger(__name__)


class AnagramFinder(object):
    """
    Anagram Finder class that finds anagrams of the words passed in as a source
    string.

    @param AnagramLangDictEnum anagram_dict_enum: Enum which defines the
            Anagram Dictionary to use.
    """

    def __init__(self, anagram_dict_enum=AnagramLangDictEnum.EN_US_WEBSTER):
        """
        @param AnagramLangDictEnum anagram_dict_enum: Enum which defines the
                Anagram Dictionary to use.
        """
        log.debug("Initialising dictionary: %r", anagram_dict_enum)
        if anagram_dict_enum is AnagramLangDictEnum.EN_US_WEBSTER:
            self.anagram_lang_dict = EnUsWebster()
        elif anagram_dict_enum is AnagramLangDictEnum.SOURCE_FILE:
            self.anagram_lang_dict = SourceFile()

    def get_anagram_lists(self, contents):
        """Return a list of sorted anagrams without any duplicates.

        @param str contents: String from a `file.read()` call.
        @returns: list of anagram tuples.
        """
        filtered_words = filter_source_str(contents)

        anagram_list = []
        for word in filtered_words:
            anagrams = self.anagram_lang_dict.get_anagrams(word, contents)
            if anagrams:
                anagram_list.append(anagrams)

        if not anagram_list:
            return [("no anagrams found", )]

        # Filter out duplicate anagrams.
        filtered_anagram_list = filter_anagram_lists(anagram_list)
        return filtered_anagram_list
