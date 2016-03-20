#!/usr/bin/env python
# coding: utf-8

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui, QtNetwork
from SlippyMap import SlippyMap


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
    w.setWindowTitle("OpenStreetMap")

    w.resize(600, 450)

    w.show()
    sys.exit(app.exec_())
