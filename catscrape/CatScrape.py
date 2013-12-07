#!/usr/bin/env python
import extractors

class CatScrape:
        def __init__(self):
                self.extractorList = extractors.gen_extractors()


        def findExtractor(self, url):
                """
                Accepts a URL and asks each extractor if it can handle it.
                Returns a list of extractors that can handle the URL.
                @param url: URL of the image/album/etc to be downloaded.
                """
                validExtractors = list()
                for extractor in self.extractorList:
                    print(extractor)
                    if extractor.check_url(url):
                        print('MATCH! %s' % url)
                    else:
                        print('Nope')

c = CatScrape()
c.findExtractor("ele")
c.findExtractor("http://imgur.com/a/9HFbU")
