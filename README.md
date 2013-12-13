Catscrape
=========
[![Build Status](https://travis-ci.org/Jaiz909/catscrape.png?branch=master)](https://travis-ci.org/Jaiz909/catscrape)

Multithreaded imgur album downloader. The imgur album download link compiles a zip archive and seems to take a long time
on some albums. The download link usually doesn't preserve the order of the original album. Catscrape will quickly
pull images from an imgur album into a new directory, preserving the order of the album.

Requirements
--------
* Python 2.7, 3.2 or 3.3
* Beautifulsoup 4 (Will be installed automatically if it isn't present)

Installation
--------
Run either `make install` or `python setup.py install` as root.

Usage
--------
```
usage: catscrape [-h] [-d] [-q] -a ALBUM [-o OUTDIR] [-n NUMTHREADS]

optional arguments:
  -h, --help     show this help message and exit
  -d             Enable debugging output
  -q             Enable quiet mode
  -a ALBUM       The imgur album url to download images from.
  -o OUTDIR      The directory to save images to. Defaults to the album id in
                 the current working directory.
  -n NUMTHREADS  The number of threads to use for downloading. Default=10.

```
