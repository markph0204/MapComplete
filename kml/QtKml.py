#!/usr/bin/env python
# coding: utf-8

from PyQt4 import QtCore, QtGui, QtXml

class KmlHandler(QtXml.QXmlDefaultHandler):
    def __init__(self, root):
        QtXml.QXmlDefaultHandler.__init__(self)
        self._error = ""

    def fatalError(self, exception):
        print('Parse Error: line %d, column %d:\n  %s' % (
              exception.lineNumber(),
              exception.columnNumber(),
              exception.message(),
              ))
        return False

    def errorString(self):
        return self._error    


if __name__ == '__main__':
    file = QtCore.QFile("../resources/continents.kml");
    file.open(QtCore.QIODevice.ReadOnly)

    doc = QtXml.QDomDocument("mydocument");
    doc.setContent(file)

    docElem = doc.documentElement();

    kml = docElem.firstChild()
    Document = kml.firstChild()
    print Document.toElement().nodeName()

    # while (n):
    #     e = n.toElement()
    #     if not e.isNull():
    #         print e.nodeName()
    #     n = n.nextSibling()




    # if file.open())
    #     return;
    # if ( notdoc.setContent(&file)) {
    #     file.close();
    #     return;
    # }
    # file.close();    