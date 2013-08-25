catscrape
=========

Downloads albums from imgur.com

Usage
--------
usage: catscrape.py [-h] -a ALBUM [-o OUTDIR] [-n NUMTHREADS]

optional arguments:
  -h, --help     show this help message and exit
  -a ALBUM       The imgur album url to download images from.
  -o OUTDIR      The directory to save images to. Defaults to the album id in
                 the current working directory.
  -n NUMTHREADS  The number of threads to use for downloading. Default=10.

