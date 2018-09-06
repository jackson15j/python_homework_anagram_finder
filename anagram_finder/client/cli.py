from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum

import click
import json
import logging
# import urllib
import requests

log = logging.getLogger(__name__)


class Cli(object):
    """CLI Client class that makes a GET REST API request to the AnagramFinder
    service and then renders the results to the console (One anagram list per
    line).
    """
    def __init__(self, base_path="http://127.0.0.1:5000"):
        self.base_path = base_path

    def input(self, filename, dictionary=None):
        """Wrapper function that:

        * Reads in the input file.
        * Selects REST path from selected input dictionary.
        * Does AnagramFinder GET request.
        * Calls `printer()` to display to stdout.

        # TODO: separate out LHS file read and RHS network activity.
        # TODO: use enums for dictionary, now that the input checking has been
        # separated out.

        @param str filename: File path to a file containing words that anagrams
                need to be found for.
        @param str dictionary: Name of dictionary to use.
        """
        # TODO: check file is not empty. Failure error code.
        with open(filename, 'r') as infile:
            f = infile.read()

        log.debug(
            "Dictionary: %r, Filename: %r, Content: %r", dictionary, filename,
            f)

        path = "%s/anagrams/%s" % (self.base_path, dictionary)
        if dictionary is None:
            path = "%s/anagrams/%s" % (self.base_path, 'en-us-webster')

        log.debug(path)
        # urllib library
        # response = urllib.request.urlopen("%s/%s" % (path, f))
        # content = response.read().decode('utf-8')

        # FIXME: Use query form in request: "url?query_string", instead of:
        # "url/query_string".

        # requests library.
        response = requests.get("%s/%s" % (path, f))
        content = response.content.decode('utf-8')
        # TODO: add response code check.
        log.debug(content)

        anagram_lists = json.loads(content)
        log.debug(anagram_lists)
        self.printer(anagram_lists)

    def printer(self, anagram_lists):
        """Munges the input into a list of anagrams per line. Which is then
        printed to stdout.

        @param list anagram_lists: Expects output from:
                `AnagramFinder().get_anagram_lists()`.
        """
        for anagram_list in anagram_lists:
            click.echo(" ".join(anagram_list))


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option(
    '--dictionary',
    type=click.Choice([
        'en-us-webster',
        'source-file'
    ]))
def input(filename, dictionary=None):
    return Cli().input(filename, dictionary)


def main():
    """Main entrypoint for the Anagram Finder application. Uses the CLI client.
    """
    log.debug("Calling CLI instance...")
    input()
    log.debug("Application exit.")


if __name__ == '__main__':
    main()
