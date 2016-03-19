#!/usr/bin/env python

import sip
sip.setapi('QVariant', 2)

import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from Point import Point
from TileOperations import *


rad = 6

class TrackPoint(QGraphicsEllipseItem):

    def __init__(self, path, index):
        super(TrackPoint, self).__init__(-rad, -rad, 2*rad, 2*rad)

        self.rad = rad
        self.path = path
        self.index = index
        
        self.setZValue(1)

        self.setBrush(Qt.white)
        self.setPen(Qt.red)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.path.updateElement(self.index, value)
        return QGraphicsEllipseItem.itemChange(self, change, value)

    def paint(self, painter, option, widget):
        if option.state & QStyle.State_MouseOver:
            painter.setBrush(Qt.gray)
        super(TrackPoint, self).paint(painter, option, widget)

    def mousePressEvent(self, event):
        self.update()
        super(TrackPoint, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(TrackPoint, self).mouseReleaseEvent(event)




class LineString(QGraphicsPathItem):
    def __init__(self, path, scene):
        super(LineString, self).__init__(path)
        self.path = path
        for i in xrange(path.elementCount()):
            node = TrackPoint(self, i)
            node.setPos(QPointF(path.elementAt(i)))
            scene.addItem(node)
        
        pen = QPen(Qt.red, 1.75)
        pen.setCosmetic(True)
        self.setPen(pen)     
        
    def updateElement(self, index, pos):
        self.path.setElementPositionAt(index, pos.x(), pos.y())
        self.setPath(self.path)




class MapScene(QGraphicsScene):

    updated = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self, view):
        super(MapScene, self).__init__(view)

        self._offset = QtCore.QPoint()
        self._tilesRect = QRect()
        self._tilePixmaps = {}


        self._emptyTile = QPixmap(TDIM, TDIM)
        self._emptyTile.fill(Qt.lightGray)



        self._url = QUrl()
        self._manager = QNetworkAccessManager()   #############

        cache = QNetworkDiskCache()
        cache.setCacheDirectory(
            QDesktopServices.storageLocation
                (QDesktopServices.CacheLocation))
        self._manager.setCache(cache)
        self._manager.finished.connect(self.handleNetworkData)


    def invalidate(self):
        view = self.parent()
        zoom = view.zoom
        rect = view.mapToScene(view.viewport().rect()).boundingRect()
        center = rect.center()

        ct = tileForCoordinate(center.y(), center.x(), zoom)
        tx = ct.x()
        ty = ct.y()

        xp = int(self.parent().width() / 2 - (tx - math.floor(tx)) * TDIM)
        yp = int(self.parent().height() / 2 - (ty - math.floor(ty)) * TDIM)

        # first tile vertical and horizontal
        xa = (xp + TDIM - 1) / TDIM
        ya = (yp + TDIM - 1) / TDIM
        xs = int(tx) - xa
        ys = int(ty) - ya

        # offset for top-left tile
        self._offset = QtCore.QPoint(xp - xa * TDIM, yp - ya * TDIM)

        # last tile vertical and horizontal
        xe = int(tx) + (self.parent().width() - xp - 1) / TDIM
        ye = int(ty) + (self.parent().height() - yp - 1) / TDIM

        # build a rect
        self._tilesRect = QtCore.QRect(xs, ys, xe - xs + 1, ye - ys + 1)

        if self._url.isEmpty():
             self.download()

        self.updated.emit(QtCore.QRect(0, 0, self.parent().width(), self.parent().height()))


    def drawBackground(self, painter, rect):
        for x in range(self._tilesRect.width()):
            for y in range(self._tilesRect.height()):
                tp = Point(x + self._tilesRect.left(), y + self._tilesRect.top())
                box = QtCore.QRect(self.tileRect(tp))
                if rect.intersects(QtCore.QRectF(box)):
                    tile = self._tilePixmaps.get(tp, self._emptyTile)
                    area = self.parent().mapToScene(box).boundingRect().toRect()
                    print "Area", area
                    painter.drawPixmap(area, tile)                    

    def handleNetworkData(self, reply):
        img = QImage()
        tp = Point(reply.request().attribute(QNetworkRequest.User))
        url = reply.url()
        if not reply.error():
            if img.load(reply, None):
                img.save("last.png")
                self._tilePixmaps[tp] = QPixmap.fromImage(img)
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

        #path = 'http://tile.openstreetmap.org/%d/%d/%d.png' % (self.zoom, grab.x(), grab.y())
        path = 'https://mts2.google.com/vt?lyrs=y&x={0}&y={1}&z={2}'.format(grab.x(), grab.y(), self.parent().zoom)
        self._url = QUrl(path)
        request = QNetworkRequest()
        request.setUrl(self._url)
        request.setRawHeader('User-Agent', 'Nokia (PyQt) Graphics Dojo 1.0')
        request.setAttribute(QNetworkRequest.User, grab)
        self._manager.get(request)

    def tileRect(self, tp):
        t = tp - self._tilesRect.topLeft()
        x = t.x() * TDIM + self._offset.x()
        y = t.y() * TDIM + self._offset.y()

        return QtCore.QRect(x, y, TDIM, TDIM)        


class MapView(QGraphicsView):
    def __init__(self):
        super(MapView, self).__init__()

        scene = MapScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(-180, -90, 360, 180)

        self.setScene(scene)

        self.zoom = 5
        self.setTransform(QTransform(self.zoom,0,0,-self.zoom,0,0))

        # self.scale(self.zoom,-self.zoom)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.ScrollHandDrag)


        coords = (
        (-51.03813197260379,-29.91035059896753),
        (-50.95606810370248,-29.8572738257228 ),
        (-50.92661460776048,-29.85689211938051),
        (-50.89108115377536,-29.77213338011879),
        (-50.83985960336476,-29.73274214104657),
        (-50.83225558614762,-29.69428461538246),
        (-50.80736906730255,-29.68971315154711),
        (-50.77878735707862,-29.66149639266348)
        )

        path = QPainterPath()
        start = coords[0]
        path.moveTo(start[0], start[1])

        for c in coords[1:]:
            path.lineTo(c[0], c[1]);

        scene.addItem(LineString(path, scene))
            
        # self.fitInView(path.boundingRect(), Qt.KeepAspectRatio)

        self.setMinimumSize(400, 400)
        self.setWindowTitle("Map Application")

        self.scene().invalidate()

    def itemMoved(self):
        # ??
        pass

    # def mouseMoveEvent(self, event):
    #     self.scene().invalidate()
    #     super(MapView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.scene().invalidate()
        super(MapView, self).mouseReleaseEvent(event)        


    def wheelEvent(self, event):
        if(event.delta() > 0):
            self.zoom = min(self.zoom+1, 18)
        else:
            self.zoom = max(self.zoom-1, 2)

        scale = 2**(self.zoom - 1)
        self.setTransform(QTransform(scale,0,0,-scale,0,0))
        # print self.transform().m11()

        self.scene().invalidate()




if __name__ == '__main__':

    app = QApplication([])

    widget = MapView()
    widget.show()

    app.exec_()
