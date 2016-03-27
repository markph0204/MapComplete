#!/usr/bin/env python

import sip
sip.setapi('QVariant', 2)

import math

from PyQt4 import QtCore, QtGui, QtNetwork
from lib.Point import Point
from lib.tileOperations import *

TDIM = 256


class LightMaps(QtGui.QWidget):
    def __init__(self, parent = None):
        super(LightMaps, self).__init__(parent)

        self.pressed = False
        self.snapped = False
        self._map = SlippyMap(self)
        self.pressPos = QtCore.QPoint()
        self.dragPos = QtCore.QPoint()
        self._map.updated.connect(self.updateMap)

    def setCenter(self, lat, lng):
        self._map.latitude = lat
        self._map.longitude = lng
        self._map.invalidate()

    def updateMap(self, r):
        self.update(r)


    def resizeEvent(self, event):
        self._map.width = self.width()
        self._map.height = self.height()
        self._map.invalidate()

    def paintEvent(self, event):
        p = QtGui.QPainter()
        p.begin(self)
        self._map.render(p, event.rect())
        p.setPen(QtCore.Qt.black)
        p.end()


    def mousePressEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return

        self.pressed = self.snapped = True
        self.pressPos = self.dragPos = event.pos()

    def mouseMoveEvent(self, event):
        if not event.buttons():
            return

        if not self.pressed or not self.snapped:
            delta = event.pos() - self.pressPos
            self.pressPos = event.pos()
            self._map.pan(delta)
            return
        else:
            threshold = 10
            delta = event.pos() - self.pressPos
            if self.snapped:
                self.snapped &= delta.x() < threshold
                self.snapped &= delta.y() < threshold
                self.snapped &= delta.x() > -threshold
                self.snapped &= delta.y() > -threshold

        self.dragPos = event.pos()


    def mouseReleaseEvent(self, event):
        self.update()


    def wheelEvent(self, event):
        delta = event.delta()
        delta = abs(delta)/delta
        self._map.change_zoom(delta)
        self.update();


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self._map.pan(QtCore.QPoint(20, 0))
        if event.key() == QtCore.Qt.Key_Right:
            self._map.pan(QtCore.QPoint(-20, 0))
        if event.key() == QtCore.Qt.Key_Up:
            self._map.pan(QtCore.QPoint(0, 20))
        if event.key() == QtCore.Qt.Key_Down:
            self._map.pan(QtCore.QPoint(0, -20))
        if event.key() == QtCore.Qt.Key_Z or event.key() == QtCore.Qt.Key_Select:
            self.dragPos = QtCore.QPoint(self.width() / 2, self.height() / 2)


class SlippyMap(QtCore.QObject):

    updated = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self, parent=None):
        super(SlippyMap, self).__init__(parent)

        self._offset = QtCore.QPoint()
        self._tilesRect = QtCore.QRect()
        self._tilePixmaps = {} # Point(x, y) to QPixmap mapping

        self._manager = TileDownloader(self) ##QtNetwork.QNetworkAccessManager()   #############
        #self._manager.finished.connect(self.handleNetworkData)
        self._url = QtCore.QUrl()

        # public vars
        self.width = 400
        self.height = 300
        self.zoom = 7
        self.latitude = -30
        self.longitude = -51.2

        self._emptyTile = QtGui.QPixmap(TDIM, TDIM)
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
        xp = int(self.width / 2 - (tx - math.floor(tx)) * TDIM)
        yp = int(self.height / 2 - (ty - math.floor(ty)) * TDIM)

        # first tile vertical and horizontal
        xa = (xp + TDIM - 1) / TDIM
        ya = (yp + TDIM - 1) / TDIM
        xs = int(tx) - xa
        ys = int(ty) - ya

        # offset for top-left tile
        self._offset = QtCore.QPoint(xp - xa * TDIM, yp - ya * TDIM)

        # last tile vertical and horizontal
        xe = int(tx) + (self.width - xp - 1) / TDIM
        ye = int(ty) + (self.height - yp - 1) / TDIM

        # build a rect
        self._tilesRect = QtCore.QRect(xs, ys, xe - xs + 1, ye - ys + 1)

        if self._url.isEmpty():
            self._manager.download()

        self.updated.emit(QtCore.QRect(0, 0, self.width, self.height))

    def render(self, painter, rect):
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                print x, y
                tp = Point(x + self._tilesRect.left(), y + self._tilesRect.top())
                box = QtCore.QRect(self._manager.tileRect(tp))
                if rect.intersects(box):
                    print "Box", box
                    painter.drawPixmap(box, self._tilePixmaps.get(tp, self._emptyTile))

    def pan(self, delta):
        dx = QtCore.QPointF(delta) / float(TDIM)
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


class TileDownloader(QtNetwork.QNetworkAccessManager):

    updated = QtCore.pyqtSignal(QtCore.QRect)


    def __init__(self, parent=None):
        super(TileDownloader, self).__init__()

        self.parent = parent

        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory(
            QtGui.QDesktopServices.storageLocation
                (QtGui.QDesktopServices.CacheLocation))
        self.setCache(cache)

        self.finished.connect(self.handleNetworkData)

    # slots
    def handleNetworkData(self, reply):
        img = QtGui.QImage()
        tp = Point(reply.request().attribute(QtNetwork.QNetworkRequest.User))
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                self.parent._tilePixmaps[tp] = QtGui.QPixmap.fromImage(img)
        reply.deleteLater()
        self.parent.updated.emit(self.tileRect(tp))

        # purge unused tiles
        bound = self.parent._tilesRect.adjusted(-2, -2, 2, 2)
        for tp in list(self.parent._tilePixmaps.keys()):
            if not bound.contains(tp):
                del self.parent._tilePixmaps[tp]
        self.download()

    def download(self):
        grab = None
        for x in range(self.parent._tilesRect.width()):
            for y in range(self.parent._tilesRect.height()):
                tp = Point(self.parent._tilesRect.topLeft() + QtCore.QPoint(x, y))
                if tp not in self.parent._tilePixmaps:
                    grab = QtCore.QPoint(tp)
                    break

        if grab is None:
            self._url = QtCore.QUrl()
            return

        #path = 'http://tile.openstreetmap.org/%d/%d/%d.png' % (self.zoom, grab.x(), grab.y())
        path = 'https://mts2.google.com/vt?lyrs=y&x={0}&y={1}&z={2}'.format(grab.x(), grab.y(), self.parent.zoom)
        print path
        self._url = QtCore.QUrl(path)
        request = QtNetwork.QNetworkRequest()
        request.setUrl(self._url)
        request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
        request.setAttribute(QtNetwork.QNetworkRequest.User, grab)
        self.get(request)

    ################################



    def tileRect(self, tp):
        t = tp - self.parent._tilesRect.topLeft()
        x = t.x() * TDIM + self.parent._offset.x()
        y = t.y() * TDIM + self.parent._offset.y()

        return QtCore.QRect(x, y, TDIM, TDIM)


if __name__ == '__main__':

    import sys

    class MapZoom(QtGui.QMainWindow):
        def __init__(self):
            super(MapZoom, self).__init__(None)

            self.map_ = LightMaps(self)
            self.map_.setFocus()
            self.setCentralWidget(self.map_)

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('LightMaps')
    w = MapZoom()
    w.setWindowTitle("Slippy Map Demo")

    w.resize(600, 450)

    w.show()
    sys.exit(app.exec_())
