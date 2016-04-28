#!/usr/bin/env python
# coding: utf-8

import re

sample = """

-51,-29.763784,0.0 
-51.035380,-29.765178,0.0 -51.03516,-29.76529,0.0 

"""

num = "(\-?[0-9]+(\.[0-9]+)?)"
sepList = "({pat}({sep}{pat})+)"
tupl = sepList.format(pat=num, sep=',')
linestring = sepList.format(pat=tupl, sep='\s+')
coordsSpaced = "(\s*{0}\s*)".format(linestring)

for m in re.findall(coordsSpaced, sample, re.DOTALL):
    print "result"
    print m[0]
print

print re.match(coordsSpaced, sample)