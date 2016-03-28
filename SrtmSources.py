import urllib
import zipfile
from geofunctions import *

ddsUrl = 'http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/South_America/'
ddsFname = '{0}{1:02}{2}{3:03}.hgt.zip'

# dropprUrl = 'http://droppr.org/srtm/v4.1/6_5x5_TIFs/'  same fname as cgiar
cgiarUrl = "http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff/"

srtmFname = 'srtm_{}_{}.zip'


def cgiarTileFromLonLat(coords):
    lon, lat = coords
    xi = (180 + int(lon)) / 5
    yi = (60 - int(lat)) / 5
    tilename = nameformat.format(xi, yi)
    link = baseurl + tilename
    dest = './' + tilename
    urllib.urlretrieve(link, dest)
    return tilename

def ddsTileFromLonLat(coords):
    xi, yi = coords
    xstring = 'E' if xi > 0 else 'W'
    ystring = 'N' if yi > 0 else 'S'
    tilename = ddsFname.format(ystring, abs(yi), xstring, abs(xi))
    link = baseurl + ddsFname
    dest = './' + ddsFname
    urllib.urlretrieve(link, cache_path+filename)

