from abc import ABC
from abc import abstractmethod


class IAnagramLangDict(ABC):
    """Interface for Anagram finding dictionary classes. Up to the
    implementation to handle language differences.
    """

    @abstractmethod
    def get_anagrams(self, word, source_str=None):
        """Return a list of anagrams for the provided word.

        @param str word: Word to find anagrams for.
        @param str source_str: String representation of the source file or
                dictionary. Ignore if implementation defines it's own
                dictionary.
        @returns: list of anagrams strings for the provided `word` or `None`.
        """
        return NotImplementedError()
