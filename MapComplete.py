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
        mapView = MapView()
        window.setCentralWidget(mapView)
        window.show()
        sys.exit(self.exec_())


if __name__ == '__main__':

    mapComplete = MapComplete(sys.argv)