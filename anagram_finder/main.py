from anagram_finder.client import cli
from anagram_finder.utils.base_logging import BaseLogging
import logging

log = logging.getLogger(__name__)


def main():
    """Main entrypoint for the Anagram Finder application. Uses the CLI client.
    """
    BaseLogging().default_config()
    log.debug("Calling Anagram finder from CLI instance...")
    cli.input()
    log.debug("Application exit.")


if __name__ == '__main__':
    main()
