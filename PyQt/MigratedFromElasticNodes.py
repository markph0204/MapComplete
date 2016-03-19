#!/usr/bin/env python
# coding: utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


import math


class WayPoint(QGraphicsItem):
    def __init__(self):
        super(WayPoint, self).__init__()
        self._position = QPointF()


class LineString(QGraphicsItem):
    def __init__(self):
        super(LineString, self).__init__()


        #self.path = QGraphicsPathItem(linepath)

    def boundingRect(self):
        return QRectF(-30, -51, 1,1)

    def paint(self, painter, option, widget):

        scalex = painter.transform().m11()
        scaley = painter.transform().m22()

        painter.setPen(QPen(Qt.black, 1/scalex, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))
        ##self.path.paint(painter)
        ##print "painted"
        ##painter.setPen(QtCore.Qt.black)
        ##painter.setBrush(QtCore.Qt.darkGray)

        linepath = QPainterPath()
        linepath.moveTo(-30, -51)
        linepath.lineTo(-31, -52)
        linepath.lineTo(-32, -51)


        painter.drawPath(linepath)




class MapWidget(QGraphicsView):
    def __init__(self):
        super(MapWidget, self).__init__()

        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        scaleFactor = math.pow(2.0, event.delta() / 240.0)

        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)



if __name__ == '__main__':


    app = QApplication([])

    widget = MapWidget()

    widget.setSceneRect(-1000, -1000, 2000, 2000)

    ls = LineString()

    widget.scene().addItem(ls)

    #widget.scene().addRect(-50, -50, 100, 100)

    widget.show()

    app.exec_()
