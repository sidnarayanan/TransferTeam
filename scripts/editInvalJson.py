#!/usr/bin/env python

import json
from os import path
from sys import argv
from time import time

jsontest = 'invalidated.json'
j = {}
if path.isfile(jsontest):
  with open(jsontest,'r') as jsonfile:
    j = json.load(jsonfile)

with open(argv[1],'r') as infile:
  newdatasets = [l.strip() for l in list(infile)]

reason = argv[2]

j[time()] = {'reason':reason,'files':newdatasets}

with open(jsontest,'w') as jsonfile:
  json.dump(j,jsonfile)