from abc import ABC
from abc import abstractmethod
from enum import auto
from enum import Enum


class AnagramLangDictEnum(Enum):
    """Enum for Anagram dictionary selection."""
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
    EN_US_WEBSTER = auto()
    SOURCE_FILE = auto()


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
