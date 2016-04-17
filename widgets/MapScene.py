#coding:utf-8

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from lib.tileOperations import *
from lib.MapPosition import *
from tileServers.SimpleGoogleTileServer import *


class MapScene(QGraphicsScene):

    def __init__(self, view):
        super(MapScene, self).__init__(view)

        self.view = view

        self.zoomLevel = 0

        self.setSceneRect(-TILE_SIZE, -TILE_SIZE, 3*TILE_SIZE, 3*TILE_SIZE)

        self.tileServer = SimpleGoogleTileServer()
        self.tileServer.updated.connect(self.tileAvailable)

        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        ##self.addContinents()

        self.tilesToDisplay = self.createItemGroup([])

    def setModel(self, model):
        pass

    def tileAvailable(self, tilekey):
        self.invalidate()  ## it would be nice to invalidate only the appropriate tile rect


    def drawBackground(self, painter, rect):
        painter.eraseRect(rect)

        painter.drawRect(0, 0, TILE_SIZE, TILE_SIZE)

        viewport = self.view.mapToScene(self.view.viewport().geometry()).boundingRect()

        leftNormalizedCorner = viewport.left()/TILE_SIZE
        rightNormalizedCorner = viewport.right()/TILE_SIZE
        bottomNormalizedCorner = viewport.top()/TILE_SIZE
        topNormalizedCorner = viewport.bottom()/TILE_SIZE

        zoomSquare = 2**self.zoomLevel

        colFirstIndex = max(0, int(floor(zoomSquare * leftNormalizedCorner)))
        colLastIndex = min(zoomSquare - 1, int(floor(zoomSquare * rightNormalizedCorner)))

        rowFirstIndex = max(0, int(floor(zoomSquare * bottomNormalizedCorner)))
        rowLastIndex = min(zoomSquare - 1, int(floor(zoomSquare * topNormalizedCorner)))


        for row in xrange(rowFirstIndex, rowLastIndex+1):
            for col in xrange(colFirstIndex, colLastIndex+1):

                posx = float(col) * TILE_SIZE / zoomSquare
                posy = float(row + 1) * TILE_SIZE / zoomSquare
                scalex = 1.0/zoomSquare
                scaley = -1.0/zoomSquare

                tileRect = QRectF(posx,posy,TILE_SIZE*scalex,TILE_SIZE*scaley)
                intersects = tileRect.intersects(viewport)

                if not intersects:
                    continue

                painter.save()

                painter.translate(posx, posy)
                painter.scale(scalex, scaley)

                self.drawGridCell(painter, col, row)

                painter.restore()


    def drawGridCell(self, painter, col, row):
        z = self.zoomLevel
        size = 2**z
        x = col;
        y = size - row - 1

        imagename = "{}_{}_{}.jpg".format(x, y, z)
        filename = os.path.join(os.getcwd(), imagename);

        painter.drawPixmap(0, 0, self.tileServer.getTile(x,y,z))


    def add(self, kmldocument):
        for linestring in kmldocument.linestrings:
            self.addLineString(linestring.coordstring)


    def addContinents(self):
        self.addLineString("""
            -51.03813197260379,-29.91035059896753,0
            -50.95606810370248,-29.8572738257228,0
            -50.92661460776048,-29.85689211938051,0
            -50.89108115377536,-29.77213338011879,0
            -50.83985960336476,-29.73274214104657,0
            -50.83225558614761,-29.69428461538246,0
            -50.80736906730255,-29.68971315154711,0
            -50.77878735707862,-29.66149639266348,0""")

        # america do sul
        self.addLineString("""
            -68.4927034234163,-54.89173963585434,0
            -64.04026932487214,-40.43461584897202,0
            -40.91759815543567,-20.54844133960011,0
            -35.04447063728292,-6.121308246934078,0
            -61.2677039538269,9.805571069645577,0
            -77.27185149276079,9.496467740854621,0
            -81.03697722317538,-5.840627171904546,0
            -69.10898910289518,-18.40442666178684,0
            -72.39771245723382,-39.17191223838741,0
            -70.64551601799562,-52.81100623635183,0""")

        # eurasia
        self.addLineString("""
            0.8542331362648525,43.11556678425497,0
            61.88780620057599,67.50011065590442,0
            174.2545067794874,68.7262292773413,0
            137.2072259594805,50.62373164674806,0
            120.842407398942,37.75587842259501,0
            117.666152687605,25.24033633223485,0
            107.1187037518077,19.06622987106739,0
            106.4602820629654,8.246778676636218,0
            90.78471402425826,21.5957078074463,0
            77.7400396352583,7.765018334118123,0
            58.4125634036835,26.40506678721538,0
            54.45775508645003,16.73571157027779,0
            44.28125835056365,11.7117355432327,0
            34.3690499286676,27.80014670722723,0
            27.04988642171164,41.03511143283674,0
            9.52893687619893,44.30064570954608,0""")

        # australia
        self.addLineString("""
            116.5685300231295,-33.9032808497795,0
            113.4135521100377,-22.6585888214582,0
            125.7604178374558,-13.31126245282065,0
            136.1069596720315,-12.0789996208782,0
            140.4793380863889,-17.69013428501162,0
            143.0139386106011,-10.23477492658532,0
            152.0203956369053,-27.18862685258947,0
            149.6206187640659,-37.44642921559301,0
            142.2379884673926,-38.40573332521313,0
            137.8358830964679,-32.8520306002461,0
            128.8456210851458,-31.24772540973989,0
            124.0334864846231,-34.06213079807567,0
            118.4588931878781,-34.57404176310011,0""")

        # antarctica
        self.addLineString("""
            -57.36067558436248,-63.94893448537122,0
            -56.2493157212441,-75.25537269553372,0
            -32.98517673942632,-77.98911543636191,0
            -8.111004293558059,-72.40595726935356,0
            27.24332839898295,-69.53568908247821,0
            61.08824289152034,-64.4662046434793,0
            88.94815703108077,-63.96978889308209,0
            126.6396448438436,-67.11291629290221,0
            166.0708044490714,-69.82815007572854,0
            161.9039643485424,-76.16559281659255,0
            199.8065841084919,-77.22549030727043,0
            224.1735045141974,-73.40797614245443,0
            256.9456826583802,-71.65244716566102,0
            -75.18456303175634,-72.43529421868375,0
            -65.63507520385068,-65.84260710282165,0""")

        # northamerica
        self.addLineString("""
            -80.97471365812204,7.072898504597545,0
            -104.1593732016747,17.91032961549367,0
            -122.2950728495846,38.10565373437438,0
            -142.7006233940847,60.60380574281029,0
            -155.4676171949063,57.74012994334744,0
            -171.1151829922527,60.68649940662308,0
            -161.3401051714498,72.18496330118391,0
            -133.3060709063911,69.83962755846888,0
            -102.3045703523962,71.53366778717363,0
            -73.6199935104686,83.26355338813467,0
            -10.84351240606494,78.8017624443011,0
            -23.79080245113048,68.13691647233627,0
            -41.86603957501037,59.65993230445414,0
            -50.47352369413404,63.32784282116268,0
            -47.36264361197486,71.22373563599645,0
            -79.32947295325087,77.51495027770856,0
            -63.28334130859357,62.31949846985006,0
            -83.60396507314881,68.9894665715594,0
            -95.34124916900493,60.34323883694532,0
            -79.91976320960981,53.06129707770148,0
            -73.66040083032091,62.27905730917512,0
            -51.32549052627511,47.12839674630082,0
            -72.79617513850565,39.31557394822016,0
            -80.91464135339355,31.5095825797659,0
            -79.06944769431993,23.65600291370022,0
            -87.01594437634753,30.45918731194382,0
            -97.94684336489077,26.82446105991626,0
            -97.59168815261036,21.19291801981637,0
            -87.58608461732283,21.71642583209461,0
            -83.49485336708535,13.07884702915453,0""")


    def addLineString(self, kmlLineString):
        import re
        coordtuples = re.split('\s+', kmlLineString.strip())
        coords = []
        for coordtuple in coordtuples:
            coordvalues = map(float, coordtuple.split(','))
            coordvalues[0] = (coordvalues[0] + 180) % 360 - 180
            lat, lon = latlontopixels(coordvalues[1], coordvalues[0], 0)
            coords.append((lat, lon))

        path = QPainterPath()
        start = coords[0]
        path.moveTo(start[0], start[1])

        for c in coords[1:]:
            path.lineTo(c[0], c[1]);

        pathitem = QGraphicsPathItem(path)
        pen = QPen(Qt.red, 3)
        pen.setCosmetic(True)
        pathitem.setPen(pen)
        self.addItem(pathitem)


