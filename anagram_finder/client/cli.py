from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum

import click
import json
import logging
# import urllib
import requests

log = logging.getLogger(__name__)
base_path = "http://127.0.0.1:5000"


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option(
    '--dictionary',
    type=click.Choice([
        'en-us-webster',
        'source-file'
    ]))
def input(filename, dictionary=None):
    # TODO: check file is not empty. Failure error code.
    with open(filename, 'r') as infile:
        f = infile.read()

    log.debug(
        "Dictionary: %r, Filename: %r, Content: %r", dictionary, filename, f)

    path = "%s/anagrams/%s" % (base_path, dictionary)
    if dictionary is None:
        path = "%s/anagrams/%s" % (base_path, 'en-us-webster')

    print(path)
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
    printer(anagram_lists)


def printer(anagram_lists):
    """Munges the input into a list of anagrams per line. Which is then printed
    to stdout.

    @param list anagram_lists: Expects output from:
            `AnagramFinder().get_anagram_lists()`.
    """
    for anagram_list in anagram_lists:
        click.echo(" ".join(anagram_list))


def main():
    """Main entrypoint for the Anagram Finder application. Uses the CLI client.
    """
    log.debug("Calling CLI instance...")
    input()
    log.debug("Application exit.")


if __name__ == '__main__':
    main()
