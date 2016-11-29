#!/usr/bin/env python

import os, json
import sys

fin = open(sys.argv[1])

total_totalvol = 0
total_volondisk = 0

output = ''
output += '############################################################\n'
print sys.argv[1]

for line in fin:
  allblocks = set([])
  blocksondisk = set([])

  if line.strip()=='':
    continue

  cmd = 'wget -O repl.json --no-check-certificate "https://cmsweb.cern.ch/phedex/datasvc/json/prod/blockreplicas?dataset=%s&complete=y"'%(line.strip())
  #print cmd
  os.system(cmd+' >/dev/null 2>/dev/null')
  with open('repl.json','r') as fjson:
    payload = json.load(fjson)['phedex']['block']
  for b in payload:
    vol = b['bytes']
    name = b['name']
    allblocks.add((name,vol))
    for r in b['replica']:
      if 'MSS' in r['node'] or 'Buffer' in r['node']:
        continue
      blocksondisk.add((name,vol))
      break
  
  totalvol = sum([b[1] for b in allblocks])*1./10**12
  volondisk = sum([b[1] for b in blocksondisk])*1./10**12
  total_totalvol += totalvol
  total_volondisk += volondisk

  output += line
  output += '\t%i/%i blocks are complete on disk\n'%(len(blocksondisk),len(allblocks))
  output += '\t%.1f TB/%.1f TB is complete on disk\n'%(volondisk,totalvol)


print output

print 'TOTAL'
print '\t%.1f TB/%.1f TB is complete on disk'%(total_volondisk,total_totalvol)
print '############################################################'
print
print
print
