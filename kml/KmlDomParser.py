#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom
import re

"""
Every Kml file should contain the root <kml> element.

The <kml> element should contain at least one of the following possible elements:
    <NetworkLinkControl/>
    <_AbstractFeature_>
        <_AbstractStyleSelector_>
            <Style>
            <StyleMap>    
        <_AbstractContainer_>
            <Document>
                <_AbstractFeature_> ¡recursive!
            <Folder>
                <_AbstractFeature_> ¡recursive!
        <_AbstractOverlay_>
            <GroundOverlay> (Image draped over terrain)
            <PhotoOverlay> (Image to be displayed as "Street View" - that is, in 3D context)
            <ScreenOverlay> (Image fixed in the screen)
        <Placemark>


"""

class LineString(object):
    def __init__(self, linestringnode):
        self.node = linestringnode
        self.coordstring = linestringnode.getElementsByTagName("coordinates")[0].firstChild.nodeValue
        self.coords = self.parseLineStringCoordinates(self.coordstring)
        self.lats = [c[1] for c in self.coords]
        self.lons = [c[0] for c in self.coords]

    def parseLineStringCoordinates(self, coordinatestring):
        return [map(float, coord.split(',')) for coord in re.split('\s*', coordinatestring.strip())]


class Kml(object):
    def __init__(self, fname):
        
        self.content = minidom.parse(fname)
        
        kmlNode = self.content.firstChild

        if kmlNode.nodeName != "kml":
            raise

        self.processChildNodes(kmlNode)

    def processChildNodes(self, parentNode):
        
        if not parentNode.hasChildNodes:
            return

        for node in parentNode.childNodes:
            nodeName = node.nodeName

            if nodeName == "Document":
                 print "Document Found"
                 self.processChildNodes(node)

            elif nodeName == "Folder":
                print "Folder Found"
                self.processChildNodes(node)  

            elif nodeName == "GroundOverlay":
                print "GroundOverlay Found"  

            elif nodeName == "ScreenOverlay":
                print "ScreenOverlay Found"  

            elif nodeName == "PhotoOverlay":
                print "PhotoOverlay Found, but not implemented"

            elif nodeName == "Placemark":
                print
                print "PlacemarkFound"
                self.processPlacemark(node)


    def processPlacemark(self, placemark):
        for node in placemark.childNodes:
            nodeName = node.nodeName

            if nodeName == "name":
                print "Nome:", node.firstChild.nodeValue.encode('utf-8')
            if nodeName == "LineString":
                self.processLineString(node)
            else:
                print nodeName

    def processLineString(self, linestring):
        for node in linestring.childNodes:
            nodeName = node.nodeName

            if nodeName == "coordinates":
                print "coordinates found"
                                

    @property
    def linestrings(self):
        linestringNodes = self.content.getElementsByTagName("LineString")
        return [LineString(node) for node in linestringNodes]



if __name__ == '__main__':

    import matplotlib.pyplot as plt

    fname = "../resources/continents.kml"

    kml = Kml(fname)

    for linestring in kml.linestrings:
        plt.plot(linestring.lons, linestring.lats)

    plt.grid()
    plt.axis('equal')
    plt.show()

    # for ls in content.getElementsByTagName("Placemark"):
    #     lscoords = ls.getElementsByTagName('coordinates')[0].firstChild.nodeValue
    #     print parseLineStringCoordinates(lscoords)





"""
'ATTRIBUTE_NODE', 
'CDATA_SECTION_NODE', 
'COMMENT_NODE', 
'DOCUMENT_FRAGMENT_NODE', 
'DOCUMENT_NODE', 
'DOCUMENT_TYPE_NODE', 
'ELEMENT_NODE', 
'ENTITY_NODE', 
'ENTITY_REFERENCE_NODE', 
'NOTATION_NODE', 
'PROCESSING_INSTRUCTION_NODE', 
'TEXT_NODE', 

'__doc__', 
'__init__', 
'__module__', 
'__nonzero__', 
'_call_user_data_handler', 
'_child_node_types', 
'_create_entity', 
'_create_notation', 
'_elem_info', 
'_get_actualEncoding', 
'_get_async', 
'_get_childNodes', 
'_get_doctype', 
'_get_documentElement', 
'_get_documentURI', 
'_get_elem_info', 
'_get_encoding', 
'_get_errorHandler', 
'_get_firstChild', 
'_get_lastChild', 
'_get_localName', 
'_get_standalone', 
'_get_strictErrorChecking', 
'_get_version', 
'_id_cache', 
'_id_search_stack', 
'_magic_id_count', 
'_set_async', 

'abort', 
'actualEncoding', 
'appendChild', 
'async', 
'attributes', 
'childNodes', 
'cloneNode', 
'createAttribute', 
'createAttributeNS', 
'createCDATASection', 
'createComment', 
'createDocumentFragment', 
'createElement', 
'createElementNS', 
'createProcessingInstruction', 
'createTextNode', 
'doctype', 
'documentElement', 
'documentURI', 
'encoding', 
'errorHandler', 
'firstChild', 
'getElementById', 
'getElementsByTagName', 
'getElementsByTagNameNS', 
'getInterface', 
'getUserData', 
'hasChildNodes', 
'implementation', 
'importNode', 
'insertBefore', 
'isSameNode', 
'isSupported', 
'lastChild', 
'load', 
'loadXML', 
'localName', 
'namespaceURI', 
'nextSibling', 
'nodeName', 
'nodeType', 
'nodeValue', 
'normalize', 
'ownerDocument', 
'parentNode', 
'prefix', 
'previousSibling', 
'removeChild', 
'renameNode', 
'replaceChild', 
'saveXML', 
'setUserData', 
'standalone', 
'strictErrorChecking', 
'toprettyxml', 
'toxml', 
'unlink', 
'version', 
'writexml'
"""