#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom

content = minidom.parse("ogckml22.xsd")

def processNode(node):
    name = node.nodeName    
    if name == "element":        
        typeAttr = node.attributes.get('type')
        if typeAttr and typeAttr.value.startswith('kml:'):
            print "  ", typeAttr.value[4:]
        # if "name" in node.attributes:
        #     pr
        # t = child.attributes['name'].value
        # extensions = child.getElementsByTagName('extension')
        # if extensions:
        #     extension = extensions[0].attributes['base'].value.split(':')[-1]
        #     print extension
        # print t


step = 2
def traverse(node, level):
    nextlevel = level + step
    for child in node.childNodes:
        if child.nodeType != 1:
            continue
        processNode(child)
        traverse(child, nextlevel)

traverse(content.documentElement, 0)