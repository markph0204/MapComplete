#!/usr/bin/env python
# coding: utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        
        for x in xrange(0, 1000, 25):
            for y in xrange(0, 1000, 25):
                scene.addRect(x, y, 2,2)
                        
        self.setSceneRect(0,0,1000,1000)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
     
        scaleFactor = 1.15;
        if(event.delta() > 0):
            self.scale(scaleFactor, scaleFactor);
        else:
            self.scale(1.0 / scaleFactor, 1.0 / scaleFactor);
        #}
            

if __name__ == "__main__":
    
    a = QApplication([])
    view = MyGraphicsView()
    view.show()
    a.exec_()


