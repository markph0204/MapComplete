#!/usr/bin/env python
# coding: utf-8

import os
import Image
import urllib
from cStringIO import StringIO
import cairo
from geofunctions import *


class StravaTileServer(object):

    urltemplate = 'http://gometry.strava.com/tiles/cycling/color{c}/{z}/{x}/{y}.png'
    defaultpath = "../Strava Heatmap Tiles/"
    colors = {
        'blue': 6,
        'orange':  5,
        'purple-cyan': 4,
        'cyan-blue': 3
    }
    defaultcolor = 3; #colors['blue']

    def __init__(self, path='', color=None):
        self.image_cache = {}

        self.path = path if path else self.defaultpath

        ## create a cache of Cairo surfaces
        # self.surface_cache = {}

    def getTile(self, z, x, y):
        tilekey = (z, x, y, self.defaultcolor)
        if not tilekey in self.image_cache: 
            filename = '{}_{}_{}_{}.png'.format(*tilekey)
            fullname = self.path + filename
            if not os.path.isfile(fullname):
                url = self.urltemplate.format(x=x, y=y, z=z, c=self.defaultcolor)
                #print "downloading %s" % url
                urllib.urlretrieve(url, fullname)
            self.image_cache[tilekey] = Image.open(fullname)
        return self.image_cache[tilekey]


if __name__ == "__main__":
    tileserver = StravaTileServer()
    tile = tileserver.getTile(13, 2930, 4813)
    tile.show()
    
    # import matplotlib.pyplot as plt

    # plt.imshow(tile)
    # plt.show()
    
    # print 'http://gometry.strava.com/tile/cycling/color{c}/{z}/{x}/{y}.png'.format(**{'c':5, 'z': 4, 'x': 9, 'y': 4})
