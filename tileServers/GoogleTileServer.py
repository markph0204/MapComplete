#!/usr/bin/env python
# coding: utf-8

import os
import Image
import random
import urllib
import cStringIO
import cairo
from geofunctions import *


class GoogleTileServer(object):
    def __init__(self, path=''):
        self.image_cache = {}
        #self.surfdict = {}
        self.layers = 'HYBRID'

        self.path = path if path else '../Google Tiles/'
        if not os.path.exists(self.path):
             os.makedirs(self.path)
        
        self.urltemplate = 'https://mts{r}.google.com/vt?lyrs={s}&x={x}&y={y}&z={z}'
        self.layerdict = {'SATELLITE': 's', 'HYBRID': 'y', 'ROADMAP': 'r', 'TERRAIN':'t'}


    def getTile(self, z, x, y):
        tilekey = (z, x, y, self.layerdict[self.layers])
        if not tilekey in self.image_cache: 
            filename = '{}_{}_{}_{}.png'.format(*tilekey)
            fullname = self.path + filename
            if not os.path.isfile(fullname):
                url = self.urltemplate.format(x=x, y=y, z=z, s=tilekey[3], r=random.choice(range(1,4)))
                urllib.urlretrieve(url, fullname)
            self.image_cache[tilekey] = Image.open(fullname)
        return self.image_cache[tilekey]


    #def loadimage(self, fullname, tilekey):
        #im = Image.open(fullname)
        #self.imdict[tilekey] = im
        #return self.imdict[tilekey]

    #def tile_as_image(self, xi, yi, zoom):
        #tilekey = (xi, yi, zoom)
        #result = None
        #try:
            #result = self.imdict[tilekey]
        #except:
            #filename = '{}_{}_{}_{}.jpg'.format(zoom, xi, yi, self.layerdict[self.layers])
            #fullname = self.path + filename
            #try:
                #result = self.loadimage(fullname, tilekey)
            #except:
                #server = random.choice(range(1,4))
                #quadkey = tiletoquadkey(*tilekey)
                #url = self.urltemplate.format(xi, yi, zoom, self.layerdict[self.layers], server, quadkey)
                #print url
                #print "Downloading tile %s to local cache." % filename
                #urllib.urlretrieve(url, fullname)
                #result = self.loadimage(fullname, tilekey)
        #return result

    #def tile_as_surface(self, xi, yi, zoom):
        #tilekey = (xi, yi, zoom)
        #result = None
        #try:
            #result = self.surfdict[tilekey]
        #except:
            #im = self.tile_as_image(xi, yi, zoom)
            #imagestring = cStringIO.StringIO()
            #im.save(imagestring, format="PNG"); imagestring.seek(0)
            #self.surfdict[tilekey] = cairo.ImageSurface.create_from_png(imagestring)
            #result = self.surfdict[tilekey]
        #return result


if __name__ == "__main__":
    ts = GoogleTileServer('google')
    im = ts.getTile(5, 9, 4)
    im.show()
