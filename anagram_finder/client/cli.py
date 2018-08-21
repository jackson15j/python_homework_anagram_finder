from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum

import click
import logging

log = logging.getLogger(__name__)


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

    anagram_dict_enum = None
    if dictionary == 'en-us-webster':
        anagram_dict_enum = AnagramLangDictEnum.EN_US_WEBSTER
    if dictionary == 'source-file':
        anagram_dict_enum = AnagramLangDictEnum.SOURCE_FILE

    anagramFinder = (
        AnagramFinder() if anagram_dict_enum is None
        else AnagramFinder(anagram_dict_enum))
    anagram_lists = anagramFinder.get_anagram_lists(f)
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
