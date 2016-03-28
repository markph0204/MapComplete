import urllib
import zipfile
from geofunctions import *

baseurl = 'http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/South_America/{0}{1:02}{2}{3:03}.hgt.zip'

def demtilefromlonlat(coords):
    xi, yi = coords.astype(int)
    xstring = 'E' if xi > 0 else 'W'
    ystring = 'N' if yi > 0 else 'S'
    filename = tileformat.format(ystring, abs(yi), xstring, abs(xi))
    urllib.urlretrieve(baseurl+filename, cache_path+filename)


coords = numpy.array(coordfromstring('-30, -50'))

demtilefromlonlat(coords)



dss = "http://dds.cr.usgs.gov/srtm/version2_1/SRTM3/South_America/
