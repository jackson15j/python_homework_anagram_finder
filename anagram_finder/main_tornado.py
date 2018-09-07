from anagram_finder.anagram_core import AnagramFinder
from anagram_finder.dictionaries.ianagram_lang_dict import AnagramLangDictEnum
from anagram_finder.utils.base_logging import BaseLogging

from time import sleep
import json
import logging
import tornado.ioloop
import tornado.web

log = logging.getLogger(__name__)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")


class AsyncHelloHandler(tornado.web.RequestHandler):
    """TODO: Temp REST path whilst I learn tornadio. Aim is to make the
    remaining paths asynchronous.
    """
    async def get(self):
        # await a synchronous function.
        # http://www.tornadoweb.org/en/stable/faq.html#why-isn-t-this-example-with-time-sleep-running-in-parallel
        ret_val = await tornado.ioloop.IOLoop.current().run_in_executor(
            None, self._hello_delayed)
        self.write(ret_val)

    def _hello_delayed(self):
        sleep(1)
        return 'Hello World'


class AnagramsHandler(tornado.web.RequestHandler):
    def get(self):
        ret_val = "Possible anagram dictionary API paths are: %s" % ", ".join([
            "/anagrams/%s/[words]" % str(x).lower().replace('_', '-')
            for x in AnagramLangDictEnum])
        self.write(ret_val)


class AnagramsDictionaryHandler(tornado.web.RequestHandler):
    def get(self, dictionary, contents):
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
        self.write(json.dumps(anagram_lists))


def make_app():
    return tornado.web.Application([
        (r"/", HelloHandler),
        (r"/hello-async", AsyncHelloHandler),
        (r"/anagrams", AnagramsHandler),
        (r"/anagrams/(.*)/(.*)", AnagramsDictionaryHandler),
    ])


def main():
    """Main entrypoint for the Anagram Finder Server process.
    """
    BaseLogging().default_config()
    log.debug("Starting Anagram finder Server process...")
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
    log.debug("Stopping Anagram finder Server process...")


if __name__ == '__main__':
    main()
