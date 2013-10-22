#!/usr/bin/env python
"""
Author: Jai Grimshaw <jai@jaigrimshaw.com>
Date: 20130724
Filename: catscrape.py
"""

import threading
import urllib2
import urllib
import re
import os
import os.path
import argparse
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger('catscrape')

class ImgurDownloader:
        def __init__(self, savePath='.', numThreads=10):
                self.images = list()
                self.threads = list()
                self.numThreads = numThreads

                self.albumPath = savePath

                self.imgurURLRegex = re.compile('(http\:\/\/)?(\/\/)?(?P<fullURL>i\.imgur\.com\/(?P<filename>(?P<imageID>[a-zA-Z0-9]+)\.(?P<ext>jpg|jpeg|png|gif)))')

                #Prep threads. Start them after populating self.images
                for i in range(0, self.numThreads):
                        logger.debug('Prepping thread %d.', i)
                        thread = threading.Thread(target=self.downloadImage)
                        self.threads.append(thread)

        def downloadAlbum(self, url):
                match = re.match('http\:\/\/(www\.)?imgur\.com/a/([a-zA-Z0-9]+)(#[0-9]+)?', url)
                if match is None:
                        logger.error('URL does not match expected URL pattern.')
                        return None
                self.albumPath = os.path.abspath(os.path.join(self.albumPath, match.group(2)))
                try:
                        os.mkdir(self.albumPath)
                except OSError as e:
                        logger.warning('Exception thrown when creating album directory: \'%s\'', str(e))
                self.enumerateAlbum(match.group(2))

                for thread in self.threads:
                        thread.start()
                for thread in self.threads:
                        thread.join()


        def enumerateAlbum(self, albumId):
                logger.info('Enumerating album.')
                #Grab the noscript version of the URL
                album = urllib2.urlopen('http://imgur.com/a/%s/noscript' % albumId)
                logger.info('Downloaded HTML for album: \'%s\'', albumId)
                albumHTML = album.read()
                soup = BeautifulSoup(albumHTML)
                logger.info('Searching for images.')

                imageList = list() #Contains img tags
                #Images can be too small to place in a zoom div. All interesting images are in wrappers.
                imageWrappers = soup.find_all('div', class_='wrapper')
                for wrapper in imageWrappers:
                        image = wrapper.find('img')
                        if image is not None:
                                imageList.append(image)

                imageMatches = list() #Contains re.match objects
                
                for image in imageList:
                        imageLink = image.get('src', None)
                        if imageLink is None:
                                logger.warning('Image \'%s\' does not contain a src attribute. Skipping image.', str(image))
                                return

                        match = re.match(self.imgurURLRegex, imageLink)
                        imageMatches.append(match)

                #Use a count to preserve the order of the album.
                count = 0
                for match in imageMatches:
                        url = match.group('fullURL')
                        if url.startswith('http://') == False and url.startswith('https://') == False:
                                url = 'http://' + url
                        logger.info('Found: %s' % (str(url)))
                        self.images.append({'location':count, 'url':url, 'filename':match.group('filename'), 'id':match.group('imageID'), 'extension':match.group('ext')})
                        count = count + 1


        def downloadImage(self):
                #grab an image from the list until we can't.
                try:
                        while True:
                                image = self.images.pop()
                                imageLoc = image['location']
                                imageURL = image['url']
                                logger.info('Downloading: %s' % (imageURL))
                                imageFilename = image['filename']
                                urllib.urlretrieve(imageURL, os.path.join(self.albumPath, '%d_%s' % (imageLoc, imageFilename)))
                except IndexError:
                        return

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', dest='debug', action='store_true', help='Enable debugging output', default=False, required=False)
        parser.add_argument('-q', dest='quiet', action='store_true', help='Enable quiet mode', default=False, required=False)
        parser.add_argument('-a', dest='album', help='The imgur album url to download images from.', required=True)
        parser.add_argument('-o', dest='outdir', help='The directory to save images to. Defaults to the album id in the current working directory.', default='.', required=False)
        parser.add_argument('-n', dest='numthreads', help='The number of threads to use for downloading. Default=10.', type=int, default=10, required=False)
        args = parser.parse_args()
        
        logger.addHandler(logging.StreamHandler())
        if args.debug:
                logger.setLevel(logging.DEBUG)
        elif args.quiet:
                logger.setLevel(logging.CRITICAL)
        else:
                logger.setLevel(logging.INFO)


        logger.debug('Constructing downloader.')
        downloader = ImgurDownloader(savePath=args.outdir, numThreads=args.numthreads)
        logger.debug('Starting downloader.')
        downloader.downloadAlbum(url=args.album)
