#!/usr/bin/env python
# coding: utf-8

from xml.etree import ElementTree

tree = ElementTree.parse("../resources/continents.kml")


step = 2
def traverse(element, level):
    nextlevel = level + step
    for child in element:
        print ' ' * level, child.tag, child.attrib
        traverse(child, nextlevel)

traverse(tree.getroot(), 0)