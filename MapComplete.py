#coding:utf-8

import sys

import sip
sip.setapi('QVariant',2)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from widgets.MapView import *
from kml.KmlDomParser import *


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

        # create left panel (treeview)
        self.leftPanel = QTreeView()
        # create mapView()
        self.mapView = MapView()

        # create something to put the treeview and the mapview
        self.splitter = QSplitter(window)

        self.splitter.addWidget(self.leftPanel)
        self.splitter.addWidget(self.mapView)

        # set central widget as the widget that contains both
        window.setCentralWidget(self.splitter)

        window.show()
        sys.exit(self.exec_())

    def KmlFromFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("KML files (*.kml)")
        filenames = QStringList()

        if dlg.exec_():
            filename = str(dlg.selectedFiles()[0])
            kml = Kml(filename)
            self.mapView.scene().add(kml)
            ##self.leftPanel.add(kml) #### NEED TO IMPLEMENT A WAY TO "ADD" THE KML FILE TO THE TreeWidget

    def KmlFromLink(self):
        pass


if __name__ == '__main__':

    mapComplete = MapComplete(sys.argv)