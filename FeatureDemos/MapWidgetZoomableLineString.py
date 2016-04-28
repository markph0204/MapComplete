#!/usr/bin/env python
# coding: utf-8

from PySide.QtCore import *
from PySide.QtGui import *

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
        return QRect(-30, -51, 1,1) 
    
    def paint(self, painter, option, widget):

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))
        ##self.path.paint(painter)
        ##print "painted"
        ##painter.setPen(QtCore.Qt.black)
        ##painter.setBrush(QtCore.Qt.darkGray)
        
        linepath = QPainterPath()
        linepath.moveTo(-30, -51)
        linepath.lineTo(-31, -52)

        
        painter.drawPath(linepath)
        


    
class MapWidget(QGraphicsView):
    def __init__(self):
        super(MapWidget, self).__init__()

        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        #self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, event.delta() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)
        
    def addItem(self, item):
        self.scene().addItem(item)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    widget = MapWidget()
    
    widget.setSceneRect(-1000, -1000, 2000, 2000)
    
    ls = LineString()
    
    widget.addItem(ls)
    
    #widget.scene().addRect(-50, -50, 100, 100)
    
    widget.show()

    sys.exit(app.exec_())
