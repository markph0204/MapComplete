#!/usr/bin/env python
# coding: utf-8

import numpy
from math import *

EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0

def latlontopixels(coord, zoom):
    lon, lat = coord
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    my = (my * ORIGIN_SHIFT) /180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py

def pixelstolatlon(pos, zoom):
    px, py = pos
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lon, lat
    
def latlontoxy(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def xytolatlon(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

#def latlontometers(lat, lon):
    #"Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
    #mx = (lon * ORIGIN_SHIFT) / 180.0
    #my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    #my = (my * ORIGIN_SHIFT) /180.0
    #return mx, my

#def meterstolatlon(mx, my):
    #"Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"
    #lat = (my / ORIGIN_SHIFT) * 180.0
    #lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    #lon = (mx / ORIGIN_SHIFT) * 180.0
    #return lat, lon

#def pixelstometers(px, py, zoom):
    #"Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"
    #res = INITIAL_RESOLUTION / (2**zoom)
    #mx = px * res - ORIGIN_SHIFT
    #my = py * res - ORIGIN_SHIFT
    #return mx, my

#def meterstopixels(mx, my, zoom):
    #"Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"
    #res = INITIAL_RESOLUTION / (2**zoom)
    #px = (mx + ORIGIN_SHIFT) / res
    #py = (my + ORIGIN_SHIFT) / res
    #return px, py

def latlontotile(coord, zoomlevel):
    tilesize = 256
    x, y = latlontopixels(coord, zoomlevel)
    pixels = 2**zoomlevel*tilesize
    xi = int(x/tilesize)
    yi = int((pixels-y)/tilesize)
    xoff = x%tilesize
    yoff = tilesize - y%tilesize
    return numpy.array([xi, yi, xoff, yoff], dtype=int)

def coordfromstring(string):
    lat, lon = map(str.strip, string.split(','))
    return numpy.array([lon, lat], dtype=float)

def tiletoquadkey(xi, yi, z):
    quadKey = ''
    for i in range(z, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if(xi & mask) != 0:
            digit += 1
        if(yi & mask) != 0:
            digit += 2
        quadKey += str(digit)
    return quadKey


if __name__ == "__main__":
    import Image
    coords = coordfromstring('-30.722949,-52.015228')
    zoom = 12
    xi, yi, xoff, yoff = latlontotile(coords, zoom)
    quadkey = tiletoquadkey(xi, yi, zoom)
    print quadkey
