#!/usr/bin/env python
#coding:utf-8

from tileOperations import *
from math import *

class MapPosition(object):

    # __slots__ = ('_lat', '_lon')

    def __init__(self, lon, lat):

        if lon > 180 or lon < -180:
            self._lon = ((float(lon)-180) % 360) - 180
        else:
            self._lon = lon

        """
        if lat > 90 or lat < -90:
            self._lat = abs(((float(lat)-90) % 360) - 180) - 90
        else:
            self._lat = lat
        """
        l = abs(((float(lat)-90) % 360) - 180) - 90
        self._lat = max(-90, min(90, l))


    @property 
    def latitude(self):
        return self._lat

    @property 
    def longitude(self):
        return self._lon

    @property
    def lonLat(self):
        return (self._lon, self._lat)
    
    
    @staticmethod
    def fromNormalized(x, y):
        lon = x * 360 - 180
        lat = y * 180 - 90
        return MapPosition(lon, lat)

    def getPixelCoords(self, zoomLevel):
        mx = (self._lon * ORIGIN_SHIFT) / 180.0
        a = tan((90 + self._lat) * pi/360.0)
        # if a == 0:
        #     b = 0
        # else:
        #     b = log(a)
        b = 0 if a == 0 else log(a)
        c = b / (pi/180.0)
        my = (c * ORIGIN_SHIFT) /180.0
        res = INITIAL_RESOLUTION / (2**zoomLevel)
        px = (mx + ORIGIN_SHIFT) / res
        py = (my + ORIGIN_SHIFT) / res
        return px, py        

    def getTileIndicesGoogle(self, zoomLevel):
        #return 0, 0
        x, y = self.getPixelCoords(zoomLevel)
        pixels = 2**zoomLevel*TILE_SIZE
        xi = int(x/TILE_SIZE)
        yi = int((pixels-y)/TILE_SIZE)
        return xi, yi



    def __str__ (self):
        return "Position(%.3f, %.3f)" % (self._lat, self._lon)


if __name__ == '__main__':
    
    ll = MapPosition(0,0)
    print ll
    print ll.latitude
    print ll.longitude