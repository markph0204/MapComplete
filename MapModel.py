#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

interestingElements = ['Placemark', 'Document', "Style", "StyleMap"]

class MapModel(QStandardItemModel):
    def __init__(self):
        super(MapModel, self).__init__(None)
        # self.level = 0
        # self.maxlevel = 10
        self.mapScene = None


    def addKmlFile(self, path):
        dom = minidom.parse(path)
        kmlNode = dom.firstChild
        if kmlNode.nodeName != "kml":
            raise

        item = QStandardItem()
        item.setData(kmlNode)
        kmlName = "File: " + os.path.basename(path)
        item.setText(kmlName)
        self.appendRow(item)

        self.parseNodes(item)

        self.mapScene = QGraphicsScene();


    def parseNodes(self, item):
        node = item.data()
        for subNode in node.childNodes:
            if subNode.nodeType == 1:
                newitem = CreateKmlStandardItem(subNode)
                newitem.setData(subNode)
                #newitem.setText(subNode.nodeName)
                newitem.setCheckable(True)
                item.appendRow(newitem)
                #self.parseNodes(newitem)                


def CreateKmlStandardItem(node):
    name = node.nodeName
    if name == "Document":
        return DocumentItem(node)
    elif name == "Style":
        return StyleItem(node)
    elif name == "StyleMap":
        return StyleMapItem(node)
    elif name == "Placemark":
        return PlacemarkItem(node)
    else:
        return QStandardItem()


class NodeItem(QStandardItem):
    def __init__(self, node):
        super(NodeItem, self).__init__()
        self.node = node   


class DocumentItem(NodeItem):
    def __init__(self, node):
        super(DocumentItem, self).__init__(node)
        for subNode in node.childNodes:
            name = subNode.nodeName
            if name == "name":
                print subNode.__dict__
                self.name = subNode.firstChild.data
                self.setText("Document: " + self.name)
            if name == "open":
                pass
            if name == "Style":
                pass
            if name == "StyleMap":
                pass
            if name == "Placemark":
                item = PlacemarkItem(subNode)
                self.appendRow(item)

class StyleItem(NodeItem):
    pass

class StyleMapItem(NodeItem):
    pass

class PlacemarkItem(NodeItem):
    def __init__(self, node):
        super(PlacemarkItem, self).__init__(node)
        
        for subNode in node.childNodes:
            name = subNode.nodeName
            if name == "name":                
                self.name = subNode.firstChild.data
                self.setText("Placemark: " + self.name)            