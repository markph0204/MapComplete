#!/usr/bin/env python
# coding: utf-8

from xml import sax
import pprint

class KmlHandler(sax.handler.ContentHandler):
    def __init__(self):
        self.mapping = {}


fname = "../resources/continents.kml"

open(fname)