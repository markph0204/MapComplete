#!/usr/bin/env python
# coding: utf-8

import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *


from lib.tileOperations import *


class SimpleGoogleTileServer(QObject):

    updated = pyqtSignal(tuple)

    def __init__(self):
        self.networkManager = QNetworkAccessManager()

        super(SimpleGoogleTileServer, self).__init__()

        cache = QNetworkDiskCache()
        cacheDir = QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation)
        cache.setCacheDirectory(cacheDir)
        self.networkManager.setCache(cache)

        self.networkManager.finished.connect(self.processDownloadedTile)

        self._tilePixmaps = {}
        self._tilesToDownload = set()

        self.urltemplate = 'https://mts{r}.google.com/vt?lyrs=y&x={x}&y={y}&z={z}'

        self._emptyTile = QPixmap(TILE_SIZE, TILE_SIZE)
        self._emptyTile.fill(Qt.lightGray)


    def getTile(self, x, y, z):

        tilekey = (x, y, z)

        print("SimpleGoogleTileServer.getTile({})".format(tilekey))
        print(self._tilesToDownload)

        if tilekey not in self._tilePixmaps and tilekey not in self._tilesToDownload:
            url = self.urltemplate.format(x=x, y=y, z=z, r=random.choice(range(1,4)))
            qurl = QUrl(url)
            request = QNetworkRequest()
            request.setUrl(qurl)
            request.setRawHeader(QByteArray().append('User-Agent'), QByteArray().append('Nokia (PyQt) Graphics Dojo 1.0'))
            request.setAttribute(QNetworkRequest.User, tilekey)
            self.networkManager.get(request)
            self._tilesToDownload.add(tilekey)

        return self._tilePixmaps.get(tilekey, self._emptyTile)


    def processDownloadedTile(self, reply):
        tilekey = reply.request().attribute(QNetworkRequest.User)
        url = reply.url()
        if not reply.error():
            img = QImage()
            if img.load(reply, None):
                self._tilePixmaps[tilekey] = QPixmap.fromImage(img)
                self.updated.emit(tilekey)
                if tilekey in self._tilesToDownload:
                    self._tilesToDownload.remove(tilekey)
        reply.deleteLater()
