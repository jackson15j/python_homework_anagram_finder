from client import cli

import logging


def main():
    """Main entrypoint for the Anagram Finder application. Uses the CLI client.
    """
    logging.basicConfig(
        filename='anagram_finder.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-m-%d %H:%M:%S',
        level=logging.DEBUG
    )

    logging.debug("Calling Anagram finder from CLI instance...")
    cli.input()
    logging.debug("Application exit.")


if __name__ == '__main__':
    main()
