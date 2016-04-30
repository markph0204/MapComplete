from fastkml.kml import *

fname = '../resources/continents.kml'

k = KML()

k.from_string(open(fname).read())

def plotFeatures(o):
    try:
        for feature in o.features():
            print feature
            plotFeatures(feature)
    except:
        pass

plotFeatures(k)

# for feature in k.features():
#     print feature