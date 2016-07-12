#!/usr/bin/env python

import json
from sys import argv
from time import strftime,gmtime

lfn = argv[1]
jsontest = 'invalidated.json'

with open(jsontest,'r') as infile:
  j = json.load(infile)

for time in j:
  if lfn in j[time]['files']:
    itime = int(float(time))
    print "invalidated on %s (%i)"%(strftime('%Y-%m-%d',gmtime(itime)),itime)
    print "reason: %s"%j[time]['reason']