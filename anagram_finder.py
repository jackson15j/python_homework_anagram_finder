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
