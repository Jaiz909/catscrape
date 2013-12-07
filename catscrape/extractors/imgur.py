#!/usr/bin/env python
import threading
import sys
if sys.version_info > (3, 0):
        import urllib.request, urllib.error, urllib.parse
else:
        import urllib
        import urllib2
import re
import os
import os.path
import logging
from bs4 import BeautifulSoup
logger = logging.getLogger('catscrape')

class ImgurEx:
        def __init__(self, savePath='.', numThreads=10):
                self.images = list()
                self.threads = list()
                self.numThreads = numThreads

                self.albumPath = savePath

                self.imgurImageURLRegex = re.compile('(http\:\/\/)?(\/\/)?(?P<fullURL>i\.imgur\.com\/(?P<filename>(?P<imageID>[a-zA-Z0-9]+)\.(?P<ext>jpg|jpeg|png|gif)))')
                self.imgurAlbumURLRegex = re.compile('http\:\/\/(www\.)?imgur\.com/a/([a-zA-Z0-9]+)(#[0-9]+)?')

                #Prep threads. Start them after populating self.images
                for i in range(0, self.numThreads):
                        logger.debug('Prepping thread %d.', i)
                        thread = threading.Thread(target=self.downloadImage)
                        self.threads.append(thread)


        def check_url(self, url):
            """
            Checks if this extractor can handle a url.
            @param url: The url to be tested.
            @returns: True if the url can be handled. False otherwise.
            """
            match = self.imgurAlbumURLRegex.match(url)
            if match is None:
                return False
            else:
                return True
            

        def downloadAlbum(self, url):
                match = self.imgurAlbumURLRegex.match(url)
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
                if sys.version_info > (3, 0):
                        album = urllib.request.urlopen('http://imgur.com/a/%s/noscript' % albumId)
                else:
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

                        match = re.match(self.imgurImageURLRegex, imageLink)
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
                                if sys.version_info > (3, 0):
                                        urllib.request.urlretrieve(imageURL, os.path.join(self.albumPath, '%d_%s' % (imageLoc, imageFilename)))
                                else:
                                        urllib.urlretrieve(imageURL, os.path.join(self.albumPath, '%d_%s' % (imageLoc, imageFilename)))
                except IndexError:
                        return 
