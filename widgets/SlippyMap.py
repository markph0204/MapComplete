#!/usr/bin/env python
# coding: utf-8

import sip
sip.setapi('QVariant', 2)

import math

from PyQt4 import QtCore, QtGui, QtNetwork
from lib.Point import Point
from lib.tileOperations import *


class TileDownloader(QtNetwork.QNetworkAccessManager):

    updated = QtCore.pyqtSignal(QtCore.QRect)


    def __init__(self):
        super(TileDownloader, self).__init__()

        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory(
            QtGui.QDesktopServices.storageLocation
                (QtGui.QDesktopServices.CacheLocation))
        self.setCache(cache)

        self._offset = QtCore.QPoint()
        self._tilesRect = QtCore.QRect()
        self._tilePixmaps = {} # Point(x, y) to QPixmap mapping

        self.finished.connect(self.handleNetworkData)

    ############################

    # slots
    def handleNetworkData(self, reply):
        img = QtGui.QImage()
        tp = Point(reply.request().attribute(QtNetwork.QNetworkRequest.User))
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                self._tilePixmaps[tp] = QtGui.QPixmap.fromImage(img)
        reply.deleteLater()
        self.updated.emit(self.tileRect(tp))

        # purge unused tiles
        bound = self._tilesRect.adjusted(-2, -2, 2, 2)
        for tp in list(self._tilePixmaps.keys()):
            if not bound.contains(tp):
                del self._tilePixmaps[tp]
        self.download()

    def download(self):
        grab = None
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                tp = Point(self._tilesRect.topLeft() + QtCore.QPoint(x, y))
                if tp not in self._tilePixmaps:
                    grab = QtCore.QPoint(tp)
                    break

        if grab is None:
            self._url = QtCore.QUrl()
            return

        ### NETWORK STUFF GOING ON HERE ###

        #path = 'http://tile.openstreetmap.org/%d/%d/%d.png' % (self.zoom, grab.x(), grab.y())
        path = 'https://mts2.google.com/vt?lyrs=y&x={0}&y={1}&z={2}'.format(grab.x(), grab.y(), self.zoom)
        self._url = QtCore.QUrl(path)
        request = QtNetwork.QNetworkRequest()
        request.setUrl(self._url)
        request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
        request.setAttribute(QtNetwork.QNetworkRequest.User, grab)
        self._manager.get(request)

    ################################



    def tileRect(self, tp):
        t = tp - self._tilesRect.topLeft()
        x = t.x() * TILE_SIZE + self._offset.x()
        y = t.y() * TILE_SIZE + self._offset.y()

        return QtCore.QRect(x, y, TILE_SIZE, TILE_SIZE)        


class SlippyMap(QtCore.QObject):

    updated = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self, parent=None):
        super(SlippyMap, self).__init__(parent)

        self._offset = QtCore.QPoint()
        self._tilesRect = QtCore.QRect()
        self._tilePixmaps = {} # Point(x, y) to QPixmap mapping

        self._manager = TileDownloader() ##QtNetwork.QNetworkAccessManager()   #############
        self._manager.finished.connect(self.handleNetworkData)
        self._url = QtCore.QUrl()

        # public vars
        self.width = 400
        self.height = 300
        self.zoom = 7
        self.latitude = -30
        self.longitude = -51.2

        self._emptyTile = QtGui.QPixmap(TILE_SIZE, TILE_SIZE)
        self._emptyTile.fill(QtCore.Qt.lightGray)


        ##############
        ###############

    def invalidate(self):
        if self.width <= 0 or self.height <= 0:
            return

        print self.latitude, self.longitude, self.zoom
        tx, ty = tileIndexForCoordinate(self.latitude, self.longitude, self.zoom)
        # tx = ct.x()
        # ty = ct.y()

        # top-left corner of the center tile
        xp = int(self.width / 2 - (tx - math.floor(tx)) * TILE_SIZE)
        yp = int(self.height / 2 - (ty - math.floor(ty)) * TILE_SIZE)

        # first tile vertical and horizontal
        xa = (xp + TILE_SIZE - 1) / TILE_SIZE
        ya = (yp + TILE_SIZE - 1) / TILE_SIZE
        xs = int(tx) - xa
        ys = int(ty) - ya

        # offset for top-left tile
        self._offset = QtCore.QPoint(xp - xa * TILE_SIZE, yp - ya * TILE_SIZE)

        # last tile vertical and horizontal
        xe = int(tx) + (self.width - xp - 1) / TILE_SIZE
        ye = int(ty) + (self.height - yp - 1) / TILE_SIZE

        # build a rect
        self._tilesRect = QtCore.QRect(xs, ys, xe - xs + 1, ye - ys + 1)

        if self._url.isEmpty():
            self.download()

        self.updated.emit(QtCore.QRect(0, 0, self.width, self.height))

    def render(self, painter, rect):
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                print x, y
                tp = Point(x + self._tilesRect.left(), y + self._tilesRect.top())
                box = QtCore.QRect(self.tileRect(tp))
                if rect.intersects(box):
                    print "Box", box
                    painter.drawPixmap(box, self._tilePixmaps.get(tp, self._emptyTile))

    def pan(self, delta):
        dx = QtCore.QPointF(delta) / float(TILE_SIZE)
        cx, cy = tileIndexForCoordinate(self.latitude, self.longitude, self.zoom)
        center = QtCore.QPointF(cx, cy) - dx
        self.latitude = latitudeFromTileY(center.y(), self.zoom)
        self.longitude = longitudeFromTileX(center.x(), self.zoom)
        self.invalidate()

    def change_zoom(self, val):
        self.zoom = max(1, min(22, self.zoom + val))
        print "ZOOM", self.zoom
        self.invalidate();


    ############################

    # slots
    def handleNetworkData(self, reply):
        img = QtGui.QImage()
        tp = Point(reply.request().attribute(QtNetwork.QNetworkRequest.User))
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                self._tilePixmaps[tp] = QtGui.QPixmap.fromImage(img)
        reply.deleteLater()
        self.updated.emit(self.tileRect(tp))

        # purge unused tiles
        bound = self._tilesRect.adjusted(-2, -2, 2, 2)
        for tp in list(self._tilePixmaps.keys()):
            if not bound.contains(tp):
                del self._tilePixmaps[tp]
        self.download()

    def download(self):
        grab = None
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                tp = Point(self._tilesRect.topLeft() + QtCore.QPoint(x, y))
                if tp not in self._tilePixmaps:
                    grab = QtCore.QPoint(tp)
                    break

        if grab is None:
            self._url = QtCore.QUrl()
            return

        ### NETWORK STUFF GOING ON HERE ###

        #path = 'http://tile.openstreetmap.org/%d/%d/%d.png' % (self.zoom, grab.x(), grab.y())
        path = 'https://mts2.google.com/vt?lyrs=y&x={0}&y={1}&z={2}'.format(grab.x(), grab.y(), self.zoom)
        self._url = QtCore.QUrl(path)
        request = QtNetwork.QNetworkRequest()
        request.setUrl(self._url)
        request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
        request.setAttribute(QtNetwork.QNetworkRequest.User, grab)
        self._manager.get(request)

    ################################



    def tileRect(self, tp):
        t = tp - self._tilesRect.topLeft()
        x = t.x() * TILE_SIZE + self._offset.x()
        y = t.y() * TILE_SIZE + self._offset.y()

        return QtCore.QRect(x, y, TILE_SIZE, TILE_SIZE)
