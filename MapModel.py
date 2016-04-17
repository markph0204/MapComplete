#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MapModel(QStandardItemModel):
    def __init__(self):
        super(MapModel, self).__init__(None)

    def addKml(self, path):
        dom = minidom.parse(path)
        kmlNode = dom.firstChild
        if kmlNode.nodeName != "kml":
            raise
        item = QStandardItem()
        item.setData(kmlNode)
        kmlName = self.getKmlDocumentName(kmlNode)
        item.setText(kmlName)
        self.appendRow(item)    

    def getKmlDocumentName(self, node):
        document = node.getElementsByTagName("Document")[0]
        name = document.getElementsByTagName("name")[0].firstChild.data
        return name