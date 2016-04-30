#coding:utf-8

import sys

import sip
sip.setapi('QVariant',2)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from widgets.MapView import *
from MapModel import *

class MapComplete(QApplication):

    def __init__(self, args):
        super(MapComplete, self).__init__(args)

        self.window = QMainWindow(None)
        self.setApplicationName("MapComplete")
        self.window.setWindowTitle("MapComplete")

        self.menuBar = self.window.menuBar()
        _open = self.menuBar.addMenu("Open")
        _open.addAction("KML from file...",self.KmlFromFile)
        _open.addAction("KML from link...",self.KmlFromLink)

        self.mapModel = MapModel()

        self.mapView = MapView()

        self.treeView = QTreeView()
        self.treeView.header().hide()
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)

        # self.mapView.scene().setModel(self.mapModel)
        # self.mapView.setScene(self.mapModel.mapScene)
        
        self.treeView.setModel(self.mapModel)
        self.treeView.expandAll()

        self.splitter = QSplitter(self.window)

        self.splitter.addWidget(self.treeView)
        self.splitter.addWidget(self.mapView)

        self.addContinents()

        self.window.setCentralWidget(self.splitter)

        self.window.show()
        sys.exit(self.exec_())

    def addContinents(self):   # this is temporary      
        kmlPath = "resources/continents.kml"
        self.mapModel.addKmlFile(kmlPath)

    def KmlFromFile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter("KML files (*.kml)")
        filenames = QStringList()

        if dlg.exec_():
            filename = str(dlg.selectedFiles()[0]).encode('utf-8')
            self.mapModel.addKml(MapModel)

    def KmlFromLink(self):
        # display a dialog with a textbox where the user should type or paste a valid link;
        # upon OK, if the file is valid dialog closes and link is loaded
        # otherwise an "invalid link" message is displayed and the dialog remains open
        pass


if __name__ == '__main__':

    mapComplete = MapComplete(sys.argv)