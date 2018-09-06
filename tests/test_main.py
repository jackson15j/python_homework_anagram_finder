from anagram_finder.utils.base_logging import BaseLogging
import anagram_finder

from os import path
from time import sleep
import json
import pytest
import subprocess
import logging
import requests

BaseLogging().default_config()
log = logging.getLogger(__name__)
base_module_path = path.dirname(anagram_finder.__file__)


# FIXME: Duplicated from test_anagram_finder.py.
@pytest.fixture(params=[
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


# FIXME: Duplicated from test_anagram_finder.py.
@pytest.fixture(params=[
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


# TODO: move to a central place.
@pytest.fixture(scope='class')
def anagramFinderProcess(request):
    """Spin up the AnagramFinder process."""
    cmd_backend = subprocess.Popen(
        ["pipenv", "run", "python", "main.py"],
        cwd=base_module_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    while not is_server_alive():
        sleep(0.1)

    yield

    cmd_backend.terminate()


# TODO: move to a central place.
def is_server_alive():
    """Poll check to verify the backed AnagramFinder service is running."""
    try:
        response = requests.get("http://127.0.0.1:5000/")
    except requests.ConnectionError:
        return False
    return response.status_code is 200


@pytest.mark.usefixtures('anagramFinderProcess')
class TestMain(object):
    """Integration test for the `main.py` entrypoint. The test spins up
    the AnagramFinder process explicitly for the REST API calls."""

    base_url = "http://127.0.0.1:5000/"

    def test_hello(self):
        exp = 'Hello World'
        response = requests.get(self.base_url)

        assert 200 == response.status_code
        assert exp == response.content.decode('utf-8')

    def test_anagrams(self):
        exp1 = '/anagrams/en-us-webster'
        exp2 = '/anagrams/source-file'
        response = requests.get('%sanagrams' % self.base_url)

        assert 200 == response.status_code
        assert exp1 in response.content.decode('utf-8')
        assert exp2 in response.content.decode('utf-8')

    def test_anagrams_en_us_webster(
            self,
            anagram_examples_en_us_webster_dictionary):
        src_content, exp = anagram_examples_en_us_webster_dictionary
        response = requests.get(
            '%sanagrams/en-us-webster/%s' % (self.base_url, src_content))
        ret_val = self._response_munge_hack(response)

        assert 200 == response.status_code
        assert exp == ret_val

    def test_anagrams_source_file(
            self,
            anagram_examples_source_file_dictionary):
        src_content, exp = anagram_examples_source_file_dictionary
        response = requests.get(
            '%sanagrams/source-file/%s' % (self.base_url, src_content))
        ret_val = self._response_munge_hack(response)

        assert 200 == response.status_code
        assert exp == ret_val

    def _response_munge_hack(self, response):
        """FIXME: Hack: JSON dumps/loads returns nested lists instead of our
        list of tuples.
        """
        ret_val = json.loads(response.content.decode('utf-8'))
        ret_val = [tuple(x) for x in ret_val]
        return ret_val
