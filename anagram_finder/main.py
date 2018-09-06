from anagram_finder.client import cli
from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum
from anagram_finder.utils.base_logging import BaseLogging

from flask import Flask
import json
import logging

app = Flask(__name__)
app.debug = True
app.env = 'development'
log = logging.getLogger(__name__)


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/anagrams')
def anagrams():
    ret_val = "Possible anagram dictionary API paths are: %s" % ", ".join([
        "/anagrams/%s/[words]" % str(x).lower().replace('_', '-')
        for x in AnagramLangDictEnum])
    return ret_val


@app.route('/anagrams/<path:dictionary>/<contents>')
def anagrams_dictionary(dictionary, contents):
    log.debug("XXX: ", dictionary, contents)

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
    """Main entrypoint for the Anagram Finder application. Uses the CLI client.
    """
    BaseLogging().default_config()
    log.debug("Calling Anagram finder from CLI instance...")
    cli.input()
    log.debug("Application exit.")


if __name__ == '__main__':
    # main()
    # TODO: Need a mechanism to poll that this is up and ready to serve.
    app.run()
