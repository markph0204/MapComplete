from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui

app = QtGui.QApplication([])

# # supply path to where is your qgis installed
QgsApplication.setPrefixPath("/usr", True)

# # load providers
QgsApplication.initQgis()

window = QtGui.QMainWindow()
window_frame = QtGui.QFrame(window)
window.setCentralWidget(window_frame)
frame_layout = QtGui.QGridLayout(window_frame)

canvas = QgsMapCanvas()
frame_layout.addWidget(canvas)

rasterPath = "/home/helton/Dropbox/00 Projetinhos/02 FileFormatHacks/GeoTIFF_Hacker/rs.tif"
layer = QgsRasterLayer(rasterPath, "raster")
QgsMapLayerRegistry.instance().addMapLayer(layer)
canvas_layer = QgsMapCanvasLayer(layer)
canvas.setLayerSet([canvas_layer])
canvas.setExtent(layer.extent())

window.show()
app.exec_()