import logging
import re
from imgurpython import ImgurClient
import os
import sys
import urllib
from threading import Thread
try:
    import Queue as queue
except ImportError:
    import queue as queue
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

logger = logging.getLogger('catscrape')


class ThreadPool(object):
    def __init__(self, size):
        self.threads = list()
        self.work_queue = queue.Queue()
        for _ in range(size):
            self.threads.append(Thread(target=self.do_work))

    def add_work(self, args):
        self.work_queue.put(args)

    def do_work(self):
        try:
            while True:
                args = self.work_queue.get(False)
                download_image(**args)
                self.work_queue.task_done()
        except queue.Empty:
            # Nothing left to do
            pass

    def start(self):
        for t in self.threads:
            t.start()
        # Wait for all tasks in the queue to finish
        self.work_queue.join()
        # All threads should be done
        for t in self.threads:
            t.join()
            

def download_image(url, directory, index=0):
    """
    Download an image from a url and save it into a directory, using index 
    to preserve the order in the filename.

    index: The image's index within the album.
    url: The URL to the image to be downloaded.
    directory: The path to the directory in which to save the image.
    """

    file_name = re.match(r'.*\/(?P<file_name>.*)', url).group('file_name')
    logger.debug("Downloading %s" % (url))
    if sys.version_info >= (3, 0):
        urllib.request.urlretrieve(url, os.path.join(directory, '%d_%s' % (index, file_name)))
    else:
        urllib.urlretrieve(url, os.path.join(directory, '%d_%s' % (index, file_name)))
    logger.info("Downloaded %s" % (url))

def load_config(config_path='~/.catscrape/catscrape.conf'):
    """
    Load a configuration file. If a config file does not exist, create a default one
    and throw an exception.

    config_path: Path to the configuration file. If this does not exist, create a default one.

    returns: A dictionary of config options.
    """

    path = os.path.expanduser(config_path)
    conf_dir = os.path.dirname(path)

    imgur_section = 'ImgurAPI'
    default_client_id = 'REPLACE_WITH_CLIENT_ID'
    default_client_secret = 'REPLACE_WITH_CLIENT_SECRET'

    config_parser = configparser.RawConfigParser()
    
    try:
        # If the config directory or config file do not exist, create them with default values.
        if not os.path.isdir(conf_dir):
                os.makedirs(conf_dir)
        if not os.path.isfile(path):
            with open(path, 'wb') as f:
                # If we don't already have a config. Write a default one.
                config_parser.add_section(imgur_section)
                config_parser.set(imgur_section, 'client_id', default_client_id)
                config_parser.set(imgur_section, 'client_secret', default_client_secret)
                config_parser.write(f)
            
    except OSError as e:
        logger.exception("Failed to create configuration directory in %s" % (conf_dir), e)
        raise e

    with open(path, "r") as f:
        # Read the config.
        config_parser.readfp(f)

    config = {'client_id': config_parser.get(imgur_section, 'client_id'),
            'client_secret': config_parser.get(imgur_section, 'client_secret')}

    if config['client_id'] == default_client_id or config['client_secret'] == default_client_secret:
        logger.exception("Default config detected. Please updated the config file at %s" % (path))
        raise Exception("Default config")

    # Return the config
    return config

def download_albums(album_list, output_directory, num_threads, config_path):
    """
    Download albums from album_list to output_directory.

    album_list: List containing album urls to download.
    output_directory: Directory in which to save the downloaded albums.
    num_threads: Number of concurrent downloads to perform.
    config_path: Path to an alternate config file.
    """
    # Load the configuration from specified path if set.
    if config_path:
        config = load_config(config_path)
    else:
        config = load_config()
    
    logger.debug("Connecting to Imgur")
    imgur_client = ImgurClient(config['client_id'], config['client_secret'])
    
    pool = ThreadPool(num_threads)
    
    for album_url in album_list:
        logger.debug('Downloading images from %s' % (album_url))
        album_id = re.match(r'.*\/a\/(?P<id>.*)', album_url).group('id')
        out_dir = os.path.join(output_directory, album_id)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
    
        logger.info('Downloading album %s' % (album_id))
        images = imgur_client.get_album_images(album_id)
        for index, image in enumerate(images):
            pool.add_work({'index':index, 'url':image.link, 'directory':out_dir})
    
    # Start the thread pool. Will block until all jobs are complete.
    pool.start()
