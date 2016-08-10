#!/usr/bin/env python

import os
import json
from optparse import OptionParser

usage = "usage: %prog --pattern <pattern>  [--outfile <outfile>]"
parser = OptionParser(usage=usage)
parser.add_option('-p','--pattern',action='store',type='string',default='None',dest='pattern',help='Pattern')
parser.add_option('-o','--outfile',action='store',type='string',default='stdout',dest='outfile',help='OutFile')

(opts,args) = parser.parse_args()

pattern = opts.pattern

url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?dataset=' + pattern
cmd = 'wget --no-check-certificate -O /tmp/subs.json "%s"'%url

os.system(cmd)

with open('/tmp/subs.json') as jsonfile:
  payload = json.load(jsonfile)['phedex']['dataset']

datasets = []
volume = []
for d in payload:
  datasets.append(d['name'])
  volume.append(d['bytes']/(1024*1024*1024.))

if opts.outfile=='stdout':
  for d,v in zip(datasets,volume):
    print d,v
else:
  with open(opts.outfile,'w') as outfile:
    for d,v in zip(datasets,volume):
      outfile.write('%10.2f %s\n'%(v,d))
    outfile.write('%10.2f TOTAL'%(sum(volume)))