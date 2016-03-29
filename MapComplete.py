import sys

import sip
sip.setapi('QVariant',2)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from widgets.MapView import *


class MapComplete(QApplication):

    def __init__(self, args):
        super(MapComplete, self).__init__(args)

        window = QMainWindow(None)
        self.setApplicationName("MapComplete")
        window.setWindowTitle("MapComplete")

        bar = window.menuBar()
        _open = bar.addMenu("Open")
        _open.addAction("KML from file...",self.KmlFromFile)
        _open.addAction("KML from link...",self.KmlFromLink)

        mapView = MapView()
        window.setCentralWidget(mapView)
        window.show()
        sys.exit(self.exec_())

    def KmlFromFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("KML files (*.kml)")
        filenames = QStringList()

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')

            with f:
                data = f.read()
                print data


    def KmlFromLink(self):
        pass


if __name__ == '__main__':

    mapComplete = MapComplete(sys.argv)