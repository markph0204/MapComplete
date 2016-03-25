#!/usr/bin/env python
# coding: utf-8

import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from TileOperations import *

class SimpleGoogleTileServer(QNetworkAccessManager):

    updated = pyqtSignal(tuple)


    def __init__(self):
        super(SimpleGoogleTileServer, self).__init__()

        cache = QNetworkDiskCache()
        cacheDir = QDesktopServices.storageLocation(
            QDesktopServices.CacheLocation)
        cache.setCacheDirectory(cacheDir)
        self.setCache(cache)

        self.finished.connect(self.handleNetworkData)

        self._tilePixmaps = {}

        self.tilekey = (0,0,0)

        self.urltemplate = 'https://mts{r}.google.com/vt?lyrs=y&x={x}&y={y}&z={z}'

        self._emptyTile = QPixmap(TILE_SIZE, TILE_SIZE)
        self._emptyTile.fill(Qt.lightGray)


    # slots
    def handleNetworkData(self, reply):
        img = QImage()
        tilekey = reply.request().attribute(QNetworkRequest.User)
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                self._tilePixmaps[tilekey] = QPixmap.fromImage(img)
        reply.deleteLater()

        self.updated.emit(tilekey)

        # # purge unused tiles
        # bound = self._tilesRect.adjusted(-2, -2, 2, 2)
        # for tp in list(self._tilePixmaps.keys()):
        #     if not bound.contains(tp):
        #         del self._tilePixmaps[tp]
        # self.download()




    def getTile(self, x, y, z):
        tilekey = (x, y, z)

        if tilekey not in self._tilePixmaps:
            url = self.urltemplate.format(x=x, y=y, z=z, r=random.choice(range(1,4)))
            qurl = QUrl(url)
            request = QNetworkRequest()
            request.setUrl(qurl)
            request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
            request.setAttribute(QNetworkRequest.User, tilekey)
            self.get(request)
            print "started tile download", tilekey



        """
        #if not tilekey in self.image_cache:
            filename = '{}_{}_{}.png'.format(*tilekey)
            fullname = self.path + filename
            if not os.path.isfile(fullname):
                url = self.urltemplate.format(x=x, y=y, z=z, r=random.choice(range(1,4)))
                qurl = QUrl(urlstring)
                request = QNetworkRequest()
                request.setUrl(qurl)
                request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
                request.setAttribute(QNetworkRequest.User, tilekey)

                #urllib.urlretrieve(url, fullname)
            self.image_cache[tilekey] = Image.open(fullname)
        """

        return self._tilePixmaps.get(tilekey, self._emptyTile) #image_cache[tilekey]
