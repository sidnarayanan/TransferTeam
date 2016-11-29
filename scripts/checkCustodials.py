#!/usr/bin/env python

import os, json
import sys

fin = open(sys.argv[1])

datasets = {}

for line in fin:
  cmd = 'wget -O subs.json --no-check-certificate "https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?dataset=%s&collapse=y"'%(line.strip())
  print cmd
  os.system(cmd)
  with open('subs.json','r') as fjson:
    payload = json.load(fjson)['phedex']['dataset'][0]
  for s in payload['subscription']:
    if 'MSS' in s['node']:
      node = s['node']
      if node not in datasets:
        datasets[node] = []
      datasets[node].append( (payload['name'],s['node_bytes']) )
      break

for k,v in datasets.iteritems():
  print '############################################################'
  print k
  print '\t%i datasets are custodial here'%(len(v))
  print '\tcorresponding to a total volume of %.3f TB'%(sum([vv[1] for vv in v])*1./10**12)
  for vv in v:
    print '\t\t%s'%(vv[0])
  print '############################################################'
