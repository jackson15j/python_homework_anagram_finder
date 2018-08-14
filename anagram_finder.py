from orderedset import OrderedSet
from string import punctuation
import json


class AnagramFinder(object):
    """
    Anagram Finder.

    TODO:

    * CLI class
        * Input arg validation.
        * Usage/help.
        * Create file object or read in whole file into a list?
        * Stdout printer function (UI/business logic separation);
          `printer(anagram_list)`.

    * Anagram class
        * Define dictionary source (private / instance creation).
        * `filter()` takes in file/list, splits on words, removes punctuation and
          returns a `set` of the words that were in the file.
        * `get_anagrams(word)` returns a list of anagrams or empty list?
        * TODO: Optimisation: filter the filtered_set as we get each anagram_list?
          Aim: remove words from the filtered list to save on `get_anagrams()`
          calls and a final set pass?
        * Anagram class handles iteration through file/list object to create list
          of anagrams.

    * Main class
        * Gets file/list object from CLI class.
        * Creates Anagram class instance.
        * If returned `anagram_list` is empty, `anagram_list = ["no anagrams
          found"]`.
        * calls `CLI.printer(anagram_list)`, to display.
    """
    # FIXME: move external dictionary into this project!
    # FIXME: this dictionary from: https://github.com/dwyl/english-words/ has
    # too many words that would not be considered standard. eg.
    # "stop":
    # * returns: ['opts', 'post', 'pots', 'spot', 'stop', 'tops']
    # * instead of: ['pots', 'stop', 'tops']
    #
    # or: `the`
    # * returns: ['eth', 'het', 'the']
    # * instead of: ['the']
    # default_en_dict = (
    #     "/home/craig/github_forks/english-words/words_dictionary.json")
    default_en_dict = (
        "/home/craig/github_forks/dictionary/graph.json")

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
        # Got several bugs: with my lookups:
        # FIXME: if lookups need to respect repeated chars.
        # FIXME: remove all results with chars not found in `word`.
        # FIXME: settle on a dictionary.
        anagrams = [
            x.lower() for x in self.en_dict_json.keys() if len(word) == len(x)
            and all(char in x for char in list(upper_word))]

        pluralised_anagrams = self._get_webster_pluralised_anagrams(word)
        if pluralised_anagrams:
            anagrams.extend(pluralised_anagrams)

        webster_hacks = self._get_webster_missing_eat_hack(word)
        if webster_hacks:
            anagrams.extend(webster_hacks)

        print(anagrams)

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

        * Naievely add an `s` to the end of all reduced anagrams.
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

    def _get_webster_missing_eat_hack(self, word):
        """Hack to work around the the Webster dictionary from:
        https://github.com/adambom/dictionary, not having "eat" in it.

        @param str word: Word to check if it should return "eat" as an anagram.
        @returns: `['eat']` or `None`.
        """
        if word in ['ate', 'eat', 'tea']:
            return ['eat']

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
            return [("no anagrams found")]

        # Filter out duplicate anagrams.
        filtered_anagram_list = self._filter_anagram_lists(anagram_list)
        return filtered_anagram_list


if __name__ == '__main__':
    # TODO: remove debug prints for logging.
    print("hello")
    # TODO: Remove hardcoded file.
    with open("test/data/example2.txt", 'r') as infile:
        contents = infile.read()
    print(contents)

    anagramFinder = AnagramFinder()
    anagram_lists = anagramFinder.get_anagram_lists(contents)
    print(anagram_lists)
    # TODO: print each list appropriately to stdout.
