from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui

from osgeo import gdal

# xml = """<GDAL_WMS>
#   <Service name="TMS">
#   <ServerUrl>http://tile.openstreetmap.org/${z}/${x}/${y}.png</ServerUrl>
#   </Service>
#   <DataWindow>
#     <UpperLeftX>-20037508.34</UpperLeftX>
#     <UpperLeftY>20037508.34</UpperLeftY>
#     <LowerRightX>20037508.34</LowerRightX>
#     <LowerRightY>-20037508.34</LowerRightY>
#     <TileLevel>18</TileLevel>
#     <TileCountX>1</TileCountX>
#     <TileCountY>1</TileCountY>
#     <YOrigin>top</YOrigin>
#   </DataWindow>
#   <Projection>EPSG:3857</Projection>
#   <BlockSizeX>256</BlockSizeX>
#   <BlockSizeY>256</BlockSizeY>
#   <BandsCount>3</BandsCount>
#   <Cache />
# </GDAL_WMS>"""

xml = """<GDAL_WMS>
  <Service name="TMS">
    <ServerUrl>http://mt.google.com/vt/lyrs=y&amp;x=${x}&amp;y=${y}&amp;z=${z}</ServerUrl>
  </Service>
  <DataWindow>
    <UpperLeftX>-20037508.34</UpperLeftX>
    <UpperLeftY>20037508.34</UpperLeftY>
    <LowerRightX>20037508.34</LowerRightX>
    <LowerRightY>-20037508.34</LowerRightY>
    <TileLevel>20</TileLevel>
    <TileCountX>1</TileCountX>
    <TileCountY>1</TileCountY>
    <YOrigin>top</YOrigin>      
  </DataWindow>
  <Projection>EPSG:3857</Projection>
  <BlockSizeX>256</BlockSizeX>
  <BlockSizeY>256</BlockSizeY>
  <BandsCount>3</BandsCount>
  <MaxConnections>5</MaxConnections>
  <Cache/>
</GDAL_WMS>"""

vfn = "/vsimem/wns.xml"

gdal.FileFromMemBuffer(vfn, xml)

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

# rasterPath = "~/Dropbox/00 Projetinhos/02 FileFormatHacks/GeoTIFF_Hacker/rs.tif"
# layer = QgsRasterLayer(rasterPath, "raster")
layer = QgsRasterLayer(vfn, "TileLayer")

# urlWithParams = 'url=http://wms.jpl.nasa.gov/wms.cgi&layers=global_mosaic&styles=pseudo&format=image/jpeg&crs=EPSG:4326'
# layer = QgsRasterLayer(urlWithParams, 'nasa', 'wms')

# layer_name = 'modis'
# uri = QgsDataSourceURI()
# uri.setParam('url', 'http://demo.mapserver.org/cgi-bin/wcs')
# uri.setParam("identifier", layer_name)
# layer = QgsRasterLayer(str(uri.encodedUri()), 'my wcs layer', 'wcs')

print layer.isValid()
QgsMapLayerRegistry.instance().addMapLayer(layer)
canvas_layer = QgsMapCanvasLayer(layer)
canvas.setLayerSet([canvas_layer])
canvas.setExtent(layer.extent())

window.show()
app.exec_()