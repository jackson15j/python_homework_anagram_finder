[![Build
Status](https://travis-ci.com/jackson15j/python_homework_anagram_finder.svg?branch=master)](https://travis-ci.com/jackson15j/python_homework_anagram_finder)

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
eat my tea | eat tea
do or door no no | no anagrams found
pots stop pots spot stop | pots stop spot
on pots no stop eat\nate pots spot stop tea | on no\npots stop spot\neat ate tea

Solution
========

How to Run
----------

* Using `pipenv` to manage dependencies:

```bash
pip install pipenv
pipenv install
```

* From: `anagram_finder/`, run Anagram Finder application via:

```bash
# run up the AnagramFinder server process:
pipenv run python main.py
# run the CLI Client:
pipenv run python client/cli.py [--dictionary=<anagram_dictionary>] </path/to/file.txt>
# example for anagram finding from source file:
pipenv run python client/cli.py --dictionary=source-file ../tests/data/example5.txt
```

* From: project root, run [pytest]'s via:

```bash
pipenv install -e .  # install package locally
pipenv run pytest
```

State at Point of Homework Submission
-------------------------------------

**Submitted this homework piece at tag [2018-08-15_a31a8d9_homework_submitted],
View that tag for the original state, including assumptions & PO questions.**

Current State
-------------

### Server

Synchronous AnagramFinder process (`main.py`) which exposes a REST
API. Currently hardcoded to: `http://127.0.0.1:5000/`

* `/` - GET Hello World print.
* `/anagrams` - GET List of dictionary sub-paths.
* `/anagrams/en-us-webster/<string>` - GET anagrams from provided string
  against the EN US Webster dictionary.
* `/anagrams/source-file/<string>` - GET anagrams from provided string
  against the provided string.

### Clients

Clients built on the Server API are located in the `clients/` folder.

* `cli.py` - CLI client (as specified in the original homework piece).
    * CLI can define the anagram dictionary via the optional `--dictionary`
      option.

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
	* Optimise the dictionary to improve searching. Most dictionaries are
      either flat text (word per line), CSV or JSON. _Potentially_ changing the
      structure could improve look ups. Although a cursory glance shows that
      speed increases would be for searching the initial word eg. [Wikipedia:
      Trie] (prefix tree). For Anagrams, improvements could be done by:
	      * Upfront linking all possible anagrams to each of the words in the
            anagram list. (eg. using a Trie to look up `pots`, which also
            returns `post, pots, spot, stop`.
		  * Refining the search algorithm done on a flat dictionary.
* First time using [pytest] and [pipenv]:
    * [pytest]'s fixtures are fairly powerful, like an easier to use version of
	  C#'s [xUnit] Inline/Member data annotations. For speed (and consistency
	  with the Company) I should have used [unittest], but [pytest] seems to be
	  interesting in a good way. Would like to dig more into it's feature set.
	* [pipenv] seems good for local development to quickly spin up a consistent
      environment. Can see it being useful in CI/CD situations.


[2018-08-15_a31a8d9_homework_submitted]: https://github.com/jackson15j/python_homework_anagram_finder/tree/2018-08-15_a31a8d9_homework_submitted

[RFC: 2119]: http://www.ietf.org/rfc/rfc2119

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

[xUnit]: https://xunit.github.io
[unittest]: https://docs.python.org/3/library/unittest.html
