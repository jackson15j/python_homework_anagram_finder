from anagram_finder.dictionaries.ianagram_lang_dict import IAnagramLangDict

from orderedset import OrderedSet
import logging

log = logging.getLogger(__name__)


class SourceFile(IAnagramLangDict):
    """Anagram finding class centred on using the source material to find
    Anagrams.

    .. note:: Since this is based off the source file, the Anagram list will
            be constrained compared to a dictionary look up.
    """

    def get_anagrams(self, word, source_str):
        """Return a list of anagrams for the provided word.

        @param str word: Word to find anagrams for.
        @param str source_str: String representation of the source file.
        @returns: list of anagrams strings for the provided `word` or `None`.
        """
        lower_word = word.lower()
        source_list = source_str.lower().split()
        anagrams = [
            x for x in source_list if len(word) == len(x)
            and all(char in x for char in list(lower_word))
            and all(x.count(char) == lower_word.count(char) for char in list(lower_word))
        ]
        log.debug(anagrams)

        if anagrams:
            # Note: filtering here, in case `source_str` is not filtered.
            anagrams = list(OrderedSet(anagrams))
        if len(anagrams) == 1:
            return None
        if len(anagrams) == 0:
            # FIXME: pick an appropriate exception.
            raise ValueError(
                "%r, is not in the dictionary: %r" % (word, source_str))
        # TODO: testing highlights that dictionary should remove duplicates1
        return anagrams
