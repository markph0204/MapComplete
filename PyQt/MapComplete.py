from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MapComplete(QApplication):

    def __init__(self, args):
        super(MapComplete, self).__init__(args)

        # Of course this should be the entry point were interface is
        # fleshed-out with real widgets
        self.hellobutton = QPushButton("Click MapComplete", None)
        self.hellobutton.clicked.connect(self.handleButton)
        self.hellobutton.show()

        self.exec_()    # enter event loop

    def handleButton(self):
        print ("Nice, isn't it?")
