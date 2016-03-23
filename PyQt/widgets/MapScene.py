#coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from TileServers.TileOperations import *

class MapScene(QGraphicsScene):

    updated = pyqtSignal(QRect)

    def __init__(self, view):
        super(MapScene, self).__init__(view)

    def drawBackground(self, painter, rect):
        self.drawBackgroundInSceneCoordinates(painter, rect)

    def drawBackgroundInViewCoordinates(self, painter, rect):
        zoomlevel = self.parent().zoom

        pixels = 2**zoomlevel*TILE_SIZE
        v = self.parent()
        center = v.mapToScene(v.viewport().rect()).boundingRect().center()
        pixelcenter = latlontopixels(center.y(), center.x(), zoomlevel)
        x = pixelcenter.x()
        y = pixelcenter.y()
        xi = int((pixels-y))/TILE_SIZE
        yi = int((pixels-x))/TILE_SIZE
        xoff = x%TILE_SIZE
        yoff = y%TILE_SIZE

        # ... needs to be continued


    def drawBackgroundInSceneCoordinates(self, painter, rect):
        painter.eraseRect(rect)


        painter.drawRect(0, 0, 255, 255)


        painter.save()

        ### USE TILE INFORMATION HERE INSTEAD OF THESE HARDCODED STUFF!

        tx, ty, tz = 1,2,2
        tx *= TILE_SIZE
        ty *= TILE_SIZE
        # ty *= TILE_SIZE
        painter.scale(1.0/2**tz, -1.0/2**tz)
        painter.translate(tx, -ty)
        print tx, ty, tz
        tilerect = QRect(tx, ty, TILE_SIZE, TILE_SIZE)
        # painter.drawPixmap(0, 0, self._tileManager.getTile(tx, ty, tz))

        painter.restore()



    def drawCosmeticText(self, painter, rect, string, fontsize = 0.1):
        painter.save()

        painter.translate(rect.center())

        scalex = self.parent().transform().m11()
        scaley = self.parent().transform().m22()

        painter.drawText(0, 0, QString("i"))

        font = QFont(painter.font())
        size = fontsize / self.parent().transform().m11()
        font.setPointSizeF(0.01)
        painter.setFont(font)

        painter.translate(rect.center())
        painter.scale(1,-1)

        painter.drawText(QRectF(-1000, -1000, 2000, 2000), Qt.AlignHCenter|Qt.AlignVCenter, QString("s"))

        painter.restore()

