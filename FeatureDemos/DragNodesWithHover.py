#!/usr/bin/env python

import math

from PyQt4 import QtCore, QtGui

class NodeCollection(QtGui.QGraphicsItem):
    pass

class Node(QtGui.QGraphicsItem):

    def __init__(self, graphWidget):
        super(Node, self).__init__()

        self.graph = graphWidget

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)

    def boundingRect(self):
        return QtCore.QRectF(-11, -11, 22, 22)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        gradient = QtGui.QRadialGradient(-3, -3, 10)
        if option.state & QtGui.QStyle.State_MouseOver:
            gradient.setColorAt(0, QtCore.Qt.red)
            gradient.setColorAt(1, QtCore.Qt.darkRed)
        else:
            gradient.setColorAt(0, QtCore.Qt.yellow)
            gradient.setColorAt(1, QtCore.Qt.darkYellow)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)


class ZoomableWidget(QtGui.QGraphicsView):
    def __init__(self):
        super(ZoomableWidget, self).__init__()

        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(-200, -200, 400, 400)

        self.setScene(scene)

        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        node1 = Node(self)
        node2 = Node(self)
        node3 = Node(self)

        scene.addItem(node1)
        scene.addItem(node2)
        scene.addItem(node3)

        node1.setPos(-50, -50)
        node2.setPos(0, -50)
        node3.setPos(50, -50)

        self.setMinimumSize(400, 400)
        self.setWindowTitle("Elastic Nodes")

    def itemMoved(self):
        # ??
        pass


    def wheelEvent(self, event):
        #scaleFactor = math.pow(2.0, event.delta() / 240.0)
        #factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        #if factor < 0.07 or factor > 100:
            #return
        self.scale(scaleFactor, scaleFactor)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    widget = ZoomableWidget()
    widget.show()

    sys.exit(app.exec_())
