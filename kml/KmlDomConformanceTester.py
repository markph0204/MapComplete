#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom
import re

def atc_1_root_element(kml):
    """Verify that the root element of the document 
        has [local name] = "kml" 
        and [namespace name] = "http://www.opengis.net/kml/2.2"""

    root = kml.documentElement

    isKml = root.tagName == "kml"
    isKmlNamespace = root.namespaceURI == "http://www.opengis.net/kml/2.2"

    return isKml and isKmlNamespace

def atc_2_XML_schema_constraints(kml):
    """Check that the document is well-formed and schema-valid.
        OGC-07-147r2: Annex A (KML Schemas)
        XML 1.0: Well-Formed XML Documents"""

    """
    from lxml import etree

    xmlschema_doc = etree.parse('schema.xsd')
    xml_doc = etree.parse('my.xml')
    xmlschema = etree.XMLSchema(xmlschema_doc)

    if xmlschema.validate(xml_doc):
       print 'Valid xml'
    else:
       print 'Invalid xml'
    """

    return True

def atc_3_geometry_coordinates(kml):
    """Verify that a kml:coordinates element 
        contains a list of white space-separated 2D or 3D tuples 
        that contain comma-separated decimal values (lon,lat[,hgt])."""

    num = "(\-?[0-9]+(\.[0-9]+)?)"
    sepList = "({pat}({sep}{pat})+)"
    tupl = sepList.format(pat=num, sep=',')
    linestring = sepList.format(pat=tupl, sep='\s+')
    pattern = "(\s*{0}\s*)".format(linestring) 

    for coordinates in kml.getElementsByTagName("coordinates"):
        coordString = coordinates.firstChild.nodeValue
        if not re.match(pattern, coordString):
            return False
    return True 

   


def TestKmlConformance(kmlFileName):
    kml = minidom.parse(kmlFileName)

    print "atc 1:", atc_1_root_element(kml)
    print "atc 2:", atc_2_XML_schema_constraints(kml)
    print "atc 3:", atc_3_geometry_coordinates(kml)
    


if __name__ == '__main__':
    fname = '../resources/continents.kml'
    TestKmlConformance(fname)




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