import logging


class BaseLogging(object):
    def default_config(self):
        logging.basicConfig(
            filename='anagram_finder.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-m-%d %H:%M:%S',
            level=logging.DEBUG
        )
