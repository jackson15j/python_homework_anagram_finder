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
