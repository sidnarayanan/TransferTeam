#!/usr/bin/env python

import json
from os import system
from sys import argv,exit
from re import sub
from time import time

dsname = argv[1]
system('wget --no-check-certificate -O /tmp/requestlist.json https://cmsweb.cern.ch/phedex/datasvc/json/prod/requestlist?dataset=%s > /dev/null 2>&1'%dsname)
with open('/tmp/requestlist.json') as jsonfile:
  payload = json.load(jsonfile)['phedex']['request']
requests = {}
for r in payload:
  for n in r['node']:
    requests[n['time_decided']] = (n['name'],r['type'],r['approval'],r['requested_by'])

for ts in sorted(requests):
  request= requests[ts]
  if request[1]=='xfer':
    print '[%15i]: %25s transferred to %20s (%s)'%(int(ts),request[3],request[0],request[2])
  elif request[1]=='delete':
    print '[%15i]: %25s     deleted at %20s (%s)'%(int(ts),request[3],request[0],request[2])
