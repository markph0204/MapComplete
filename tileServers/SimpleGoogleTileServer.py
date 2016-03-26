#!/usr/bin/env python
# coding: utf-8

import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from lib.tileOperations import *
#from tileServers import *

class SimpleGoogleTileServer(QNetworkAccessManager):

    updated = pyqtSignal(tuple)

    def __init__(self):
        super(SimpleGoogleTileServer, self).__init__()

        cache = QNetworkDiskCache()
        cacheDir = QDesktopServices.storageLocation(
            QDesktopServices.CacheLocation)
        cache.setCacheDirectory(cacheDir)
        self.setCache(cache)

        self.finished.connect(self.processDownloadedTile)

        self._tilePixmaps = {}

        self.tilekey = (0,0,0)

        self.urltemplate = 'https://mts{r}.google.com/vt?lyrs=y&x={x}&y={y}&z={z}'

        self._emptyTile = QPixmap(TILE_SIZE, TILE_SIZE)
        self._emptyTile.fill(Qt.lightGray)


    def getTile(self, x, y, z):

        tilekey = (x, y, z)

        if tilekey not in self._tilePixmaps:
            print tilekey
            url = self.urltemplate.format(x=x, y=y, z=z, r=random.choice(range(1,4)))
            qurl = QUrl(url)
            request = QNetworkRequest()
            request.setUrl(qurl)
            request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
            request.setAttribute(QNetworkRequest.User, tilekey)
            self.get(request)

        return self._tilePixmaps.get(tilekey, self._emptyTile) #image_cache[tilekey]


    def processDownloadedTile(self, reply):
        img = QImage()
        tilekey = reply.request().attribute(QNetworkRequest.User)
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                self._tilePixmaps[tilekey] = QPixmap.fromImage(img)
        reply.deleteLater()

        self.updated.emit(tilekey)

