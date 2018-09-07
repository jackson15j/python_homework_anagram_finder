import pytest


@pytest.fixture(scope="module", params=[
    # source_str, exp_result.
    ("the quick brown fox", [("no anagrams found", )]),
    ("eat my tea", [("eat", "tea")]),
    ("do or door no no", [("no anagrams found", )]),
    ("pots stop pots spot stop", [("pots", "spot", "stop")]),
    ("on pots no stop eat\nate pots spot stop tea",
     [("no", "on"), ("pots", "spot", "stop"), ("ate", "eat", "tea")])
])
def anagram_examples_source_file_dictionary(request):
    return request.param


@pytest.fixture(scope="module", params=[
    # source_str, exp_result.
    ("the quick brown fox", [("no anagrams found",)]),
    ("eat my tea", [("ate", "eat", "tea")]),
    ("do or door no no", [("do", "od"), ("door", "odor"), ("no", "on")]),
    ("pots stop pots spot stop", [("post", "pots", "spot", "stop")]),
    ("on pots no stop eat\nate pots spot stop tea",
     [("no", "on"), ("post", "pots", "spot", "stop"), ("ate", "eat", "tea")])
])
def anagram_examples_en_us_webster_dictionary(request):
    return request.param
