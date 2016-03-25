# coding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from TileServers.TileOperations import *
from MapScene import *


class MapView(QGraphicsView):

    MINZOOM = 0
    MAXZOOM = 20

    def __init__(self):
        super(MapView, self).__init__()

        self.configure()

        self.zoom = self.MINZOOM

        scene = MapScene(self)
        self.setScene(scene)
        self.ensureVisible(self.scene().sceneRect())


    def configure(self):
        self.setCacheMode(QGraphicsView.CacheNone)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        
        # self.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # perform zoom around mouse position
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        
        # keep centered while resizing
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        # make draggable
        self.setDragMode(QGraphicsView.ScrollHandDrag)


    def wheelEvent(self, event):
        if(event.delta() > 0):
            self.zoom = min(self.zoom+1, self.MAXZOOM)
        else:
            self.zoom = max(self.zoom-1, self.MINZOOM)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, z):
        self._zoom = z
        scale = 2**z
        translate = scale * TILE_SIZE
        self.setTransform(QTransform(scale,0,0,-scale,0,translate))
