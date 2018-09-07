from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum
from anagram_finder.utils.base_logging import BaseLogging

from flask import Flask
from time import sleep
import json
import logging

app = Flask(__name__)
app.debug = True
app.env = 'development'
log = logging.getLogger(__name__)


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/hello-async')
def hello_async():
    """TODO: Temp REST path whilst I learn asyncio/aiohttp. Aim is to make
    the remaining paths asynchronous.
    """
    return _hello_delayed()


def _hello_delayed():
    sleep(1)
    return 'Hello World'


@app.route('/anagrams')
def anagrams():
    ret_val = "Possible anagram dictionary API paths are: %s" % ", ".join([
        "/anagrams/%s/[words]" % str(x).lower().replace('_', '-')
        for x in AnagramLangDictEnum])
    return ret_val


@app.route('/anagrams/<path:dictionary>/<contents>')
def anagrams_dictionary(dictionary, contents):
    log.debug("XXX: dictionary: %r, contents: %r", dictionary, contents)

    anagram_dict_enum = None
    if dictionary == 'en-us-webster':
        anagram_dict_enum = AnagramLangDictEnum.EN_US_WEBSTER
    if dictionary == 'source-file':
        anagram_dict_enum = AnagramLangDictEnum.SOURCE_FILE

    anagramFinder = (
        AnagramFinder() if anagram_dict_enum is None
        else AnagramFinder(anagram_dict_enum))
    log.info("XXX: %r", anagramFinder)

    anagram_lists = anagramFinder.get_anagram_lists(contents)
    log.debug(anagram_lists)
    return json.dumps(anagram_lists)


def main():
    """Main entrypoint for the Anagram Finder Server process.
    """
    BaseLogging().default_config()
    log.debug("Starting Anagram finder Server process...")
    app.run()
    log.debug("Stopping Anagram finder Server process...")


if __name__ == '__main__':
    main()
