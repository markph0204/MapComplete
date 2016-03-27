# coding: utf-8

from math import floor, sqrt

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from lib import *
from MapScene import *


class MapView(QGraphicsView):

    MINZOOM = 0
    MAXZOOM = 20

    ZOOM_STEP = 0.25

    def __init__(self):
        super(MapView, self).__init__()

        self.configure()

        scene = MapScene(self)
        self.setScene(scene)
        self.ensureVisible(self.scene().sceneRect())

        self.zoomLevel = 0;

        self.setZoomLevel(0);


    def configure(self):
        self.setCacheMode(QGraphicsView.CacheNone)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.setDragMode(QGraphicsView.ScrollHandDrag)


    def wheelEvent(self, event):
        newZoomLevel = (min(self.zoomLevel + self.ZOOM_STEP, 2**self.MAXZOOM)
                        if event.delta() > 0 
                        else max(self.zoomLevel - self.ZOOM_STEP, 2**self.MINZOOM))

        self.setZoomLevel(newZoomLevel)


    def setZoomLevel(self, newZoomLevel):

        self.zoomLevel = newZoomLevel

        scale = 2**newZoomLevel
        translate = scale*TILE_SIZE
        self.setTransform(QTransform(scale,0,0,-scale,0,translate))

        self.scene().zoomLevel = int(newZoomLevel)

