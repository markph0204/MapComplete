#!/usr/bin/env python
# coding: utf-8

from PyQt4.QtCore import *

fname = "../resources/continents.kml"
file = QFile(fname)
file.open(QIODevice.ReadOnly)
xml = QXmlStreamReader(file)

while not xml.atEnd():
    xml.readNext()
    if xml.isStartElement():
        print xml.name()