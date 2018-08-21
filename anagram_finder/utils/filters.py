from orderedset import OrderedSet
from string import punctuation


def filter_anagram_lists(anagram_list):
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


def filter_source_str(contents):
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
