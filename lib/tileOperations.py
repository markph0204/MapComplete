#!/usr/bin/env python
# coding: utf-8

import math
# from PyQt4 import QtCore

"""
We have different types of "coordinates" regarding tiles:

 - Actual geographical coordinates: Latitude (lat) and Longitude (lon).
   Origin in the center of the image;
 - Pixel coordinates (px, py), referring to pixel position
   on the "full image" composed by all the tiles for a given zoom level;
 - Tile coordinates, that would be pixel coordinates divided by tile size (usually 256 pixels).

 So, at zoom level 0, we have one 256x256 tile encompassing the whole map;
 For each aditional zoom level:
     - Pixel size of full map image is doubled;
        - At zoom 1: 512x512 pixels (2x2 tiles)
        - At zoom 2: 1024x1024 pixels (4x4 tiles)
        - At zoom 3: 2014x2048 pixels (8x8 tiles)
        - At zoom N: image size is TILE_SIZE * 2**N pixels (2**N tiles per axis)
     - Amount of tiles per axis doubles;

Then we have these possible conversions between coordinates:

    latlon_to_tileindex
    tileindex_to_latlon
    latlon_to_pixel
    pixel_to_latlon
    latlon_to_tilepixel
    tilepixel_to_latlon
    tileindex_to_pixel
    pixel_to_tileindex


Best reference on the topic:
http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/

"""




TILE_SIZE = 256
EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * math.pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / TILE_SIZE
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0

def tileIndicesForLatLonBounds(start_lat, end_lat, start_lon, end_lon, zoom):
    start_lat_index = tileIndexForCoordinate(start_lat, start_lon, zoom)

def tileIndexForCoordinate(lat, lng, zoom):
    x_norm = float(lng + 180.0) / 360.0
    y_norm = (1.0 - math.log(math.tan(lat * math.pi / 180.0) +
          1.0 / math.cos(lat * math.pi / 180.0)) / math.pi) / 2.0

    # zoom_number = float(1 << zoom)
    zoom_number = 2**zoom

    return x_norm * zoom_number, y_norm * zoom_number


def longitudeFromTileX(x_norm, zoom):
    zoom_number = float(1 << zoom)
    lon = x_norm / zoom_number * 360.0 - 180.0
    return lon


def latitudeFromTileY(y_norm, zoom):
    zoom_number = float(1 << zoom)
    n = math.pi - 2 * math.pi * y_norm / zoom_number
    lat = 180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)))
    return lat

def rangeFromZoomLevel(zoom):
    pass


def latlontopixels(lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = math.log(math.tan((90 + lat) * math.pi/360.0))/(math.pi/180.0)
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



if __name__ == '__main__':
    # print tileIndexForCoordinate(-31, -51, 5)
    # print latlontopixels(-31, -51, 5)
    # print tileIndicesForLatLonBounds(start_lat, end_lat, start_lon, end_lon, zoom)
    pass