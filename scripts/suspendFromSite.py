#!/usr/bin/env python

import json,os,sys
import pycurl
import urllib
import time

# putting the functions to suspend blocks and datasets here
def updateSubscription(block, node, until):
    proxyfile='/tmp/x509up_u'+str(os.getuid())
    cadir='/etc/grid-security/certificates'

    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO,proxyfile)
    c.setopt(pycurl.CAPATH,cadir)
    c.setopt(pycurl.SSLKEY,proxyfile)
    c.setopt(pycurl.SSLCERT,proxyfile)
    
    url=str('https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&block=' + block.replace('#','%23',1) + '&node=' + node + '&suspend_until=%s'%until)
    #if debug == True : print url,pycurl.URL 
    print url
 
    c.setopt(pycurl.URL, url)
    post_data = {'block': block , 'node': node , 'suspend_until': until}

    postfields = urllib.urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

def updateSubscriptionDS(dataset, node, until):
    proxyfile='/tmp/x509up_u'+str(os.getuid())
    cadir='/etc/grid-security/certificates'

    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO,proxyfile)
    c.setopt(pycurl.CAPATH,cadir)
    c.setopt(pycurl.SSLKEY,proxyfile)
    c.setopt(pycurl.SSLCERT,proxyfile)
    
    url=str('https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&dataset=' + dataset + '&node=' + node + '&suspend_until=%s'%until)
    print url
 
    c.setopt(pycurl.URL, url)
    post_data = {'dataset': dataset , 'node': node , 'suspend_until': until}

    postfields = urllib.urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

# define some configuraton
site = sys.argv[1]
daystosuspend = int(sys.argv[2])
OVERRIDE=False

# these are the inputs - any incomplete transfers form Unified
with open('stucktape/incomplete_transfers.json') as finc:
  incomplete = json.load(finc)

# this file is a newline-separated list of datasets that should NOT be touched
if True:
  ftoexclude = open('stucktape/toprotect.txt') 
  toexclude = [x.strip() for x in ftoexclude]
else:
  toexclude = []

# this is the list of things that will be suspended (name,node,isDataset)
to_suspend = []

for k in incomplete:
  if k in toexclude:
    continue

  # first do collapse=y just to get the dataset subscriptions
  cmd = 'wget -O subs.json --no-check-certificate "https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?dataset=%s&collapse=y"'%(k)
  print cmd
  os.system(cmd + ' >/dev/null 2>/dev/null')
  with open('subs.json','r') as fsubs:
    payload = json.load(fsubs)['phedex']['dataset'][0]
  
  # first check if the custodial subscription is at the right site:
  isFromSite = False
  for s in payload['subscription']:
    if s['node']==site and s['percent_files']>99.9: 
      # check percent_files to skip some weird cases where the custodial replica is incomplete
      isFromSite = True
      break

  if not isFromSite:
    continue

  # now figure out dataset subscriptions that need suspending:
  for s in payload['subscription']:
    if 'MSS' in s['node'] or 'Buffer' in s['node']:
      continue
    if s['percent_files']>99.9:
      continue
    if (not OVERRIDE) and (s['suspended']=='y'):
      continue
    to_suspend.append( (k,s['node'],True) )

  # now do collapse=n just to get the block subscriptions
  cmd = 'wget -O subs.json --no-check-certificate "https://cmsweb.cern.ch/phedex/datasvc/json/prod/subscriptions?block=%s%%23*&collapse=n"'%(k)
  print cmd
  os.system(cmd + ' >/dev/null 2>/dev/null')
  with open('subs.json','r') as fsubs:
    payload = json.load(fsubs)['phedex']['dataset'][0]
  
  # now figure out all blocks that need suspension
  # only suspend a block if it does not exist on disk yet
  for b in payload['block']:
    bname = b['name']
    this_targets = []
    onDisk = False
    for s in b['subscription']:
      if 'MSS' in s['node'] or 'Buffer' in s['node']:
        continue # don't care about tape or buffer
      if s['level']=='DATASET':
        continue # this is actually part of a dataset-level subscription, skip
      if s['percent_files']>99.9:
        onDisk = True
        break # it's present on a disk, don't need to suspend this block
      if (not OVERRIDE) and (s['suspended']=='y'):
        continue
      this_targets.append(s['node'])
    if onDisk:
      continue
    to_suspend += [(bname,x,False) for x in this_targets]

  #if len(to_suspend)>20:
  #  break ## TEST

until = str(int(time.time() + daystosuspend*86400))
for t in to_suspend:
  if t[2]:
    updateSubscriptionDS(t[0],t[1],until)
  else:
    updateSubscription(t[0],t[1],until)
