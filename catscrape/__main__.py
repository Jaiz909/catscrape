#!/usr/bin/env python
"""
Author: Jai Grimshaw <jai@jaigrimshaw.com>
Date: 20130724
Filename: __main__.py
"""
import argparse
import logging
import catscrape_main

logger = logging.getLogger('catscrape')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ALBUM', nargs='+', help='The imgur album urls to download images from.')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enable debugging output', default=False, required=False)
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='Enable quiet mode', default=False, required=False)
    parser.add_argument('-o', '--out-dir', dest='out_dir', help='The directory to save images to. Defaults to the album id in the current working directory.', default='.', required=False)
    parser.add_argument('-n', '--num-threads', dest='num_threads', help='The number of threads to use for downloading. Default=10.', type=int, default=10, required=False)
    parser.add_argument('-c', '--conf-file', dest='config_path', help='The path to the configuration file.', type=file, default=None, required=False)
    args = parser.parse_args()
    
    # Set up logging.
    sh =  logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(sh)
    if args.debug:
            logger.setLevel(logging.DEBUG)
    elif args.quiet:
            logger.setLevel(logging.CRITICAL)
    else:
            logger.setLevel(logging.INFO)
    catscrape_main.download_albums(args.ALBUM, args.out_dir, args.num_threads, args.config_path)

if __name__ == '__main__':
        main()
