Catscrape
=========
[![Build Status](https://travis-ci.org/Jaiz909/catscrape.png?branch=master)](https://travis-ci.org/Jaiz909/catscrape)

Multithreaded imgur album downloader. The imgur album download link compiles a zip archive and seems to take a long time
on some albums. The download link usually doesn't preserve the order of the original album. Catscrape will quickly
pull images from an imgur album into a new directory, preserving the order of the album.

Requirements
--------
* Python 2.7, 3.2 or 3.3

Installation
--------
Run either `make install` or `python setup.py install`.

Usage
--------
```
usage: catscrape [-h] [-d] [-q] [-o OUT_DIR] [-n NUM_THREADS] [-c CONFIG_PATH]
                 ALBUM [ALBUM ...]

positional arguments:
  ALBUM                 The imgur album urls to download images from.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debugging output
  -q, --quiet           Enable quiet mode
  -o OUT_DIR, --out-dir OUT_DIR
                        The directory to save images to. Defaults to the album
                        id in the current working directory.
  -n NUM_THREADS, --num-threads NUM_THREADS
                        The number of threads to use for downloading.
                        Default=10.
  -c CONFIG_PATH, --conf-file CONFIG_PATH
                        The path to the configuration file.
```
