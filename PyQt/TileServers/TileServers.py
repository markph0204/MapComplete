#!/usr/bin/env python
# coding: utf-8

import os
import Image
import random
import urllib
import cStringIO
import cairo
from geofunctions import *


class TileServer(object):
    def __init__(self, servertype, path=''):
        self.imdict = {}
        self.surfdict = {}
        self.layers = 'HYBRID'

        if servertype == 'google':
            self.path = '../Google Tiles/'
            self.urltemplate = 'https://mts{4}.google.com/vt?lyrs={3}&x={0}&y={1}&z={2}'
            self.layerdict = {'SATELLITE': 's', 'HYBRID': 'y', 'ROADMAP': 'r', 'TERRAIN':'t'}

        elif servertype == 'bing':
            self.path = '../Bing Tiles/'
            self.urltemplate = 'http://ecn.t{4}.tiles.virtualearth.net/tiles/{3}{5}?g=0'
            self.layerdict = {'SATELLITE': 'a', 'HYBRID': 'h', 'ROADMAP': 'r'}

        if path:
            self.path = path

    def loadimage(self, fullname, tilekey):
        im = Image.open(fullname)
        self.imdict[tilekey] = im
        return self.imdict[tilekey]

    def tile_as_image(self, xi, yi, zoom):
        tilekey = (xi, yi, zoom)
        result = None
        try:
            result = self.imdict[tilekey]
        except:
            filename = '{}_{}_{}_{}.jpg'.format(zoom, xi, yi, self.layerdict[self.layers])
            fullname = self.path + filename
            try:
                result = self.loadimage(fullname, tilekey)
            except:
                server = random.choice(range(1,4))
                quadkey = tiletoquadkey(*tilekey)
                url = self.urltemplate.format(xi, yi, zoom, self.layerdict[self.layers], server, quadkey)
                print url
                print "Downloading tile %s to local cache." % filename
                urllib.urlretrieve(url, fullname)
                result = self.loadimage(fullname, tilekey)
        return result

    def tile_as_surface(self, xi, yi, zoom):
        tilekey = (xi, yi, zoom)
        result = None
        try:
            result = self.surfdict[tilekey]
        except:
            im = self.tile_as_image(xi, yi, zoom)
            imagestring = cStringIO.StringIO()
            im.save(imagestring, format="PNG"); imagestring.seek(0)
            self.surfdict[tilekey] = cairo.ImageSurface.create_from_png(imagestring)
            result = self.surfdict[tilekey]
        return result


if __name__ == "__main__":
    ts = TileServer('google')
    im = ts.tile_as_image(1,2,2)
    im.show()
