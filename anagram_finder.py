from string import punctuation


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
    # TODO: add tests!!
    def _filter_anagram_lists(self, anagram_list):
        """Sorts and filters the nested anagram list to remove duplicates.

        @param list anagram_list: Nested list of unsorted anagram lists.
        @returns: `set()` of anagram lists.
        """
        [x.sort() for x in anagram_list]
        return set([tuple(x) for x in anagram_list])

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
        ret_val = set(ret_val.split())
        return ret_val

    def _get_anagrams(self, word):
        """Return a list of anagrams for the provided word.

        @todo :: Anagram logic.

        @param str word: Word to find anagrams for.
        @returns: list of anagrams strings for the provided `word`.
        """
        # TOOD: investigate how to pull in a dictionary to do anagram logic.
        print(word)
        if word == 'my':
            return ["banana", "jam"]
        return ["stock", "list"]

    def get_anagram_lists(self, contents):
        """Return a list of sorted anagrams without any duplicates.

        @param str contents: String from a `file.read()` call.
        @returns: `set()` of anagram lists.
        """
        filtered_words = self._filter_source(contents)

        anagram_list = []
        for word in filtered_words:
            anagrams = self._get_anagrams(word)
            anagram_list.append(anagrams)

        # Filter out duplicate anagrams.
        anagram_set = self._filter_anagram_lists(anagram_list)
        return anagram_set


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
