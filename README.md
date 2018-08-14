Homework: Anagram Finder
========================

This is my solution to a homework problem for an; Anagram Finder, application.

Requirements
------------

* Input:
    * `<file>.txt` as an argument.
* Output:
    * Stdout.
	* No Anagrams in the file: `"no anagrams found"`.
	* All anagrams for a particular word should be on a single line of stdout.
	* All anagrams for the next unique word should be on a new line.
	* Assumption: Examples show no repeats for any repeated words (or any words
      that are found in the _"found"_ anagrams list).
	* Anagrams printed in file read order.

Notes
-----

* User does not provide a dictionary.
* Anagrams are for each specific word on, not phrases / collections of words.

Expectation
-----------

INPUT | OUPUT
------|-------
the quick brown fox | no anagrams found
eat my tea | eat eat
do or door no no | no anagrams found
pots stop pots spot stop | pots stop spot
on pots no stop eat |
ate pots spot stop tea | on no
 | pots stop spot
 | eat ate tea

Solution
========

How to Run
----------

* Using `pipenv` to manage dependencies:

```bash
pip install pipenv
cd anagram_finder/
pipenv install
```

* From: `anagram_finder/`, run Anagram Finder application via:

```bash
pipenv run python main.py </path/to/file.txt>
```

* From: `anagram_finder/`, run [pytest]'s via:

```bash
pipenv run pytest
```


Questions for Product Owner
---------------------------

Here are the list of questions, with assumptions/reasoning, that I would have
asked on this homework task:

* Should anagrams be done locally or use an external online service?
* Examples are given in English. Assuming English for anagram look ups?
* Homework from a British company that does majority of business with the
  USA and then UK/Australia. Should the spellings be GB English or US English?
* There are inconsistencies in the anagrams listed in the examples. Are these
  explicit mistakes to incite questions or genuine mistakes?
     * `eat my tea`, expects: `eat tea`, but instead there should be: `ate eat
       tea`.
     * `do or door no no`, expects: `no anagrams found`, but instead there
       should be: `no on`, for all English dictionaries. Webster US English
       also lists: `do od`, and: `odor door`, as valid anagrams.
	 * `pots stop pots spot stop`, expects: `pots stop spot`, but instead there
       should be: `post pots spot stop`
* Is a single blocking script an acceptable solution, or should it be an
  asynchronous anagram finding service (which exposes an API) that multiple
  Client UI's can connect to?
* Client-side request to response time is not stated. Is there a maximum
  threshold?
* Algorithm complexity is not stated. Is there a preferred complexity for the
  anagram finder solution? And if there is, is it mandatory even if a poorly
  optimised solution is still within Client-side time thresholds above?
* Should the solution be designed from the point of view of a standalone piece
  of work (that is not touched when completed) or with the expectation that
  additional work could be done in the future?

### Assumptions:

* Anagram results in English.
* Anagram finding done from a local dictionary.
* Inconsistencies in the examples provided can be ignored if dictionary source
  provides valid _additional_ anagrams.
* US English is _acceptable_ as a solution (due to above note on business
  priorities) if a suitable GB English dictionary can not be found.
* Un-requested Enhancement: parse out punctuation - on assumption that source
  files may have punctuation.
* Un-requested Enhancement: lower case source to avoid potential duplication -
  on assumption that source files may have a mixture of casing.

Current State
-------------

* Backend, synchronous `AnagramFinder()` class that exposes a single getter for
  accepting a string and returning a nested list of anagrams or `no anagrams
  found`.
    * This class has some unittests.
	* Hard-coded to use [Github: Webster's Dictionary] (US English) (Does have
      an uppercase JSON representation as well as a graph representation) (Only
      found out it was US English late in testing due to anagram candidates
      after a bug fix (`door`, `odor`)).
	* Functional anagram finding but not optimised greatly (Reduces dictionary
      to targets that are the same length as the source word. Second reduction
      to targets that contain source words' characters. Final reduction to the
      correct count of source words' characters).
* Client-side CLI that creates an instance of `AnagramFinder()`. This UI
  handles the file reading into a string as input to the `AnagramFinder()`
  getter as well as manipulating the getter output into the appropriate form to
  display on stdout.
* Entrypoint in `main.py` which is hard coded to call the Client-side CLI.
    * Integration tests to verify the Client-side CLI with real example files.



Future Plans
------------

...Or things I'd do if I had more time:

* Find an _appropriate_ GB English dictionary. Requires further investigation,
  but potential solutions include (Note: had rejected remote dictionaries due
  to Assumption listed above):
    * [Github: english-words] - Local dictionary - tried initially. Has too
      many words I'd consider non-dictionary terms. Does have a lowercase JSON
      representation though. Unsure if it is GB or US English.
    * [Github: EnglishDictionaryAPI] - Remote dictionary - Web scraping of
      Merriam-Webster and Thesaurus.com - not in pypy. Unsure if it is GB or US
      English.
	* [Oxford Dictionaries API] - Remote dictionary - REST API. GB English.
	* [Brian Kelk: Wordlists] - Local dictionary - **Worth
      investigating**. Found whilst compiling this list and thinking of
      client/server spell checkers like [Aspell] and [Hunspell. Loads of word
      list resources including an [UK_English_wordlist.zip] which includes
      frequency.
    * `pip search dictionary` - local/remote dictionaries - 100 hits with ~1/3
      at a quick glance that look like language dictionaries. **Requires more
      investigation**.
	* OS level / package manager dictionary - local dictionary - ignored due to
      cross-platform worries over location/availability.
* Update the backend `AnagramFinder()` to be an asynchronous process that
  exposes a REST API, so that it can handle multiple clients.
    * Also allow dictionary to be configured or User provided. The latter is
      harder, since there is not a great deal of standardisation from my
      current investigations (txt, JSON (differing schema's), CSV, REST), as
      well as quality in dictionaries (to much garbage vs. missing expected
      words vs. handling of pluralisation).
	* Optimise the dictionary to improve searching. Most dictionaries are
      either flat text (word per line), CSV or JSON. _Potentially_ changing the
      structure could improve look ups. Although a cursory glance shows that
      speed increases would be for searching the initial word eg. [Wikipedia:
      Trie] (prefix tree). For Anagrams, improvements could be done by:
	      * Upfront linking all possible anagrams to each of the words in the
            anagram list. (eg. using a Trie to look up `pots`, which also
            returns `post, pots, spot, stop`.
		  * Refining the search algorithm done on a flat dictionary.
* Update Client-side CLI so that it runs in a separate process and uses the
  backends REST API.
    * _Potentially_ add other Client-side UI's (WebUI, emacs/vim...).
* Add project to an external CI, such as [Travis] or [Jenkins].
* First time using [pytest] and [pipenv]:
    * [pytest]'s fixtures are fairly powerful, like an easier to use version of
	  C#'s [xUnit] Inline/Member data annotations. For speed (and consistency
	  with the Company) I should have used [unittest], but [pytest] seems to be
	  interesting in a good way. Would like to dig more into it's feature set.
	* [pipenv] seems good for local development to quickly spin up a consistent
      environment. Can see it being useful in CI/CD situations.


[pipenv]: https://docs.pipenv.org
[pytest]: https://docs.pytest.org/en/latest/index.html

[Github: Webster's Dictionary]: https://github.com/adambom/dictionary
[Github: english-words]: https://github.com/dwyl/english-words/
[Github: EnglishDictionaryAPI]: https://github.com/SaiWebApps/EnglishDictionaryAPI
[Oxford Dictionaries API]: https://developer.oxforddictionaries.com/documentation
[Brian Kelk: Wordlists]: http://www.bckelk.ukfsn.org/menu.html#Wordlists
[Aspell]: http://aspell.net
[Hunspell]: hunspell.github.io
[UK_English_wordlist.zip]: http://www.bckelk.ukfsn.org/words/wlist.zip
[Wikipedia: Trie]: https://en.wikipedia.org/wiki/Trie

[Travis]: https://travis-ci.com
[Jenkins]: https://jenkins.io
[xUnit]: https://xunit.github.io
[unittest]: https://docs.python.org/3/library/unittest.html
