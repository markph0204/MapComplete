from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

a = QApplication(sys.argv)
view = QGraphicsView()

view.setRenderHint(QPainter.Antialiasing)
view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
view.setDragMode(QGraphicsView.ScrollHandDrag)

scene = QGraphicsScene(view)
scene.setBackgroundBrush(Qt.yellow)

view.setScene(scene)

rect = QGraphicsRectItem(-51, -30, 10, 10)
#rect.setBrush(QBrush(Qt.darkRed))
scene.addItem(rect)

linepath = QPainterPath()
linepath.moveTo(-51, -30)
linepath.lineTo(-31, -52)

scene.addItem(QGraphicsPathItem(linepath))


scene.setSceneRect(-1000, -1000, 3000, 3000)

view.centerOn(-50, -30)


view.show()
sys.exit(a.exec_())
