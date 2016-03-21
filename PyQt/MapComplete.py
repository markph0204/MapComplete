from PyQt4.QtGui import *
from PyQt4.QtCore import *

from widgets.MapView import *


class MapComplete(QApplication):

    def __init__(self, args):
        super(MapComplete, self).__init__(args)

        # TODO: should use QMainWindow?
        widget = MapView()
        widget.show()

        self.exec_()


if __name__ == '__main__':
    import sys
    from MapComplete import MapComplete

    mapComplete = MapComplete(sys.argv)