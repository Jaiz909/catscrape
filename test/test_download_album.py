import unittest
import hashlib
import tempfile
import os
import os.path
import sys
sys.path.append('..')
import catscrape

class TestAlbumDownload(unittest.TestCase):
        def setUp(self):
                self.albumURL = 'http://imgur.com/a/9HFbU'
                self.albumID = '9HFbU'
                self.expectedFiles = list()
                self.expectedFiles.append({'url':'http://i.imgur.com/ASd2V0U.gif', 'filename':'0_ASd2V0U.gif', 'md5':'f8f88b8ac12c71ee40b952c87eb4b3fa'})
                self.expectedFiles.append({'url':'http://i.imgur.com/dHO0Lzz.jpg', 'filename':'1_dHO0Lzz.jpg', 'md5':'5cf89cfab1174a62cc095a396fcf09bf'})
                self.expectedFiles.append({'url':'http://i.imgur.com/UsFSHdD.jpg', 'filename':'2_UsFSHdD.jpg', 'md5':'f815af133e66b9c6a5ea7073ea9af52a'})

        def testDiscovery(self):
                i = catscrape.ImgurDownloader(savePath=tempfile.mkdtemp())
                i.enumerateAlbum(albumId=self.albumID)
                notFound = self.expectedFiles

                foundURLs = list()
                for image in i.images:
                        foundURLs.append(image['url'])

                for e in notFound:
                        self.assertIn(e['url'], foundURLs)


        def testFiles(self):
                downloadDir = tempfile.mkdtemp()
                i = catscrape.ImgurDownloader(savePath=downloadDir)
                i.downloadAlbum(url=self.albumURL)

                albumPath = os.path.join(downloadDir, self.albumID)
                downloadedFiles = os.listdir(albumPath)
                notFound = self.expectedFiles
                for e in self.expectedFiles:
                        self.assertIn(e['filename'], downloadedFiles)
                        with open(os.path.join(albumPath, e['filename']), 'rb') as f:
                                h = hashlib.md5()
                                h.update(f.read())
                                self.assertEqual(h.hexdigest(), e['md5'])

if __name__ == '__main__':
        unittest.main()
