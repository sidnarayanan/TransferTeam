#!/usr/bin/env python

import os, json
import sys

# fin = open(sys.argv[1])

total_totalvol = 0
total_volondisk = 0

output = ''
output += '############################################################\n'

for line in [sys.argv[1]]:
  allblocks = {}
  blocksondisk = {}
  custodial = {}

  if line.strip()=='':
    continue

  print 'PATTERN: %s'%(line.strip())

  blockpattern = '/%s/RunIISummer15wmLHEGS-MCRUN2_71_V1-v1*/GEN-SIM%%23*'%(line.strip())

  cmd = 'wget -O repl.json --no-check-certificate "https://cmsweb.cern.ch/phedex/datasvc/json/prod/blockreplicas?block=%s&complete=y"'%(blockpattern)
  os.system(cmd+' >/dev/null 2>/dev/null')
  with open('repl.json','r') as fjson:
    payload = json.load(fjson)['phedex']['block']
  for b in payload:
    vol = b['bytes']
    name = b['name']
    dsname = name.split('#')[0]
    if dsname not in allblocks:
      allblocks[dsname] = set([])
      blocksondisk[dsname] = set([])
      custodial[dsname] = 'UNKNOWN'
    allblocks[dsname].add((name,vol))
    for r in b['replica']:
      if 'MSS' in r['node'] or 'Buffer' in r['node']:
        custodial[dsname] = r['node'].replace('_MSS','').replace('_Buffer','')
        continue
      blocksondisk[dsname].add((name,vol))
      break
  
  for dsname in allblocks:
    totalvol = sum([b[1] for b in allblocks[dsname]])*1./10**12
    volondisk = sum([b[1] for b in blocksondisk[dsname]])*1./10**12
    total_totalvol += totalvol
    total_volondisk += volondisk

    print  dsname
    print '\tcustodial at %s'%custodial[dsname] 
    print '\t%i/%i blocks are complete on disk'%(len(blocksondisk[dsname]),len(allblocks[dsname]))
    print '\t%2g TB/%2g TB is complete on disk'%(volondisk,totalvol)

# print output

# print 'TOTAL'
# print '\t%.1f TB/%.1f TB is complete on disk'%(total_volondisk,total_totalvol)
# print '############################################################'
# print
# print
# print
