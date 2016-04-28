#!/usr/bin/env python
# coding: utf-8

from xml.dom import minidom

content = minidom.parse("../resources/continents.kml")

step = 2
def traverse(node, level):
    nextlevel = level + step
    for child in node.childNodes:
        if child.nodeType != 1:
            continue
        print ' ' * level, child.nodeName
        traverse(child, nextlevel)

traverse(content.documentElement, 0)