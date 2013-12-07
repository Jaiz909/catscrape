#!/usr/bin/env python
"""
Author: Jai Grimshaw <jai@jaigrimshaw.com>
Date: 20130724
Filename: __main__.py
"""
import argparse
import logging
from extractors.imgur import ImgurEx

logger =logging.getLogger('catscrape')

def main():
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
        downloader = ImgurEx(savePath=args.outdir, numThreads=args.numthreads)
        logger.debug('Starting downloader.')
        downloader.downloadAlbum(url=args.album)

if __name__ == '__main__':
        main()
