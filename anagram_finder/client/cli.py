from anagram_finder.anagram_core import AnagramFinder

import click
import logging

log = logging.getLogger(__name__)


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def input(filename):
    # TODO: check file is not empty. Failure error code.
    with open(filename, 'r') as infile:
        f = infile.read()

    log.debug("Filename: %r, Content: %r", filename, f)
    anagramFinder = AnagramFinder()
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
