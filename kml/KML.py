#!/usr/bin/env python
# coding: utf-8

class AbstractObject(object)
    def __init__(self):
        self.id = None;

class Kml(object):
    def __init__(self):
        self.networkLinkControl = None
        self.abstractFeature = None
        self.simpleExtensions = []
        self.objectExtensions = []

class AbstractFeature(AbstractObject):
    pass

class NetworkLinkControl(object):
    pass

class Object(object):
    def __init__(self, _id = ""):
        self.id = _id

class Feature(Object):
    def __init__(self):
        self.name = ""
        self.visibility = True
        self.open = False
        self.description = ""
        self.styleUrl = ""

class Geometry(Object):
    pass

class Placemark(Feature):
    """A Placemark is a Feature with associated Geometry"""
    def __init__(self):
        self.Geometry = None

class LineString(Geometry):
    def __init__(self):
        self.coordinates = []

class KmlDocument(object):
    pass
    # def __init__(self):
    #     self.name = ""
    #     self.visibility = True
    #     self.open = False
    #     self.address = ""

        
    