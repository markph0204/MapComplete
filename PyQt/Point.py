#!/usr/bin/env python

import sip
sip.setapi('QVariant', 2)

#import sys
#import math

from PyQt4 import QtCore, QtGui, QtNetwork

class Point(QtCore.QPoint):
    """QPoint, that is fully qualified as a dict key"""
    def __init__(self, *par):
        if par:
            super(Point, self).__init__(*par)
        else:
            super(Point, self).__init__()

    def __hash__(self):
        return self.x() * 17 ^ self.y()

    def __repr__(self):
        return "Point(%s, %s)" % (self.x(), self.y())
