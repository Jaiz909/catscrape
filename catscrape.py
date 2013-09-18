#!/usr/bin/python
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


class ImgurDownloader:
	def __init__(self, savePath='.', numThreads=10):
		self.images = list()
		self.threads = list()
		self.numThreads = numThreads

		self.albumPath = savePath

		#Prep threads. Start them after populating self.images
		for _ in range(0, self.numThreads):
			thread = threading.Thread(target=self.downloadImage)
			self.threads.append(thread)

	def downloadAlbum(self, url):
		match = re.match('http\:\/\/(www\.)?imgur\.com/a/([a-zA-Z0-9]+)(#[0-9]+)?', url)
		self.albumPath = os.path.abspath(os.path.join(self.albumPath, match.group(2)))
		os.mkdir(self.albumPath)
		self.enumerateAlbum(match.group(2))

		for thread in self.threads:
			thread.start()


	def enumerateAlbum(self, albumId):
		#Grab the noscript version of the URL
		album = urllib2.urlopen('http://imgur.com/a/%s/noscript' % albumId)
		albumHTML = album.read()
		#NEVER USE REGEX TO PARSE HTML. THIS WILL SUMMON LUCIFER HIMSELF.
		imageMatches = re.findall('<img src="(?P<fullURL>http\:\/\/i\.imgur\.com\/(?P<filename>(?P<imageID>[a-zA-Z0-9]+)\.(?P<ext>jpg|jpeg|png|gif)))', albumHTML)
		#Use a count to preserve the order of the album.
		count = 0
		for match in imageMatches:
			self.images.append({'location':count, 'url':match[0], 'filename':match[1], 'id':match[2], 'extension':match[3]})
			count = count + 1


	def downloadImage(self):
		#grab an image from the list until we can't.
		try:
			while True:
				image = self.images.pop()
				imageLoc = image['location']
				imageURL = image['url']
				imageFilename = image['filename']
				urllib.urlretrieve(imageURL, os.path.join(self.albumPath, '%d_%s' % (imageLoc, imageFilename)))
		except IndexError:
			return

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', dest='album', help='The imgur album url to download images from.', required=True)
	parser.add_argument('-o', dest='outdir', help='The directory to save images to. Defaults to the album id in the current working directory.', default='.', required=False)
	parser.add_argument('-n', dest='numthreads', help='The number of threads to use for downloading. Default=10.', type=int, default=10, required=False)
	args = parser.parse_args()

	downloader = ImgurDownloader(savePath=args.outdir, numThreads=args.numthreads)
	downloader.downloadAlbum(url=args.album)
