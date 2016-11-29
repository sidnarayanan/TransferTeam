#!/usr/bin/env python

import json
from os import system
from sys import exit
from re import sub
import time
import os
import pycurl
import urllib
from StringIO import StringIO

until = int(time.mktime(time.strptime('2016-07-28','%Y-%m-%d')))
debug=True

def updateSubscription(block, node, until):
#    print block,node
    proxyfile='/tmp/x509up_u'+str(os.getuid())
    cadir='/etc/grid-security/certificates'

    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO,proxyfile)
    c.setopt(pycurl.CAPATH,cadir)
    c.setopt(pycurl.SSLKEY,proxyfile)
    c.setopt(pycurl.SSLCERT,proxyfile)
    
#    ds = block.split('#')[0]
#    url=str('https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&dataset=' + ds + '&node=' + node + '&suspend_until='+str(until))
    url=str('https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&block=' + block.replace('#','%23',1) + '&node=' + node + '&suspend_until='+str(until))
 
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, lambda x : None)
    post_data = {'block': block , 'node': node , 'suspend_until': str(until)}
    #post_data = {'dataset': ds , 'node': node , 'suspend_until': str(until)}

    postfields = urllib.urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

def checkSubscription(block,node):
    proxyfile='/tmp/x509up_u'+str(os.getuid())
    cadir='/etc/grid-security/certificates'

    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO,proxyfile)
    c.setopt(pycurl.CAPATH,cadir)
    c.setopt(pycurl.SSLKEY,proxyfile)
    c.setopt(pycurl.SSLCERT,proxyfile)
    
    ds = block.split('#')[0]
    url=str('https://cmsweb.cern.ch/phedex/datasvc/perl/prod/subscriptions?collapse=n&nocache=1&dataset=' + ds + '&node=' + node)
    print url
 
    s = StringIO('')

    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEFUNCTION, s.write)
    post_data = {'dataset': ds , 'node': node }

    postfields = urllib.urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

    print s.getvalue()
    #payload = json.load(s)
    #print payload


with open('/afs/cern.ch/user/d/dmytro/public/forSid/transfer_backlog.json','r') as fjson:
  payload = json.load(fjson)

counter=0
for rid in payload:
  for block in payload[rid]:
    for targetsite in payload[rid][block]:
      print targetsite,block,counter
      updateSubscription(block,targetsite,str(until))
#      checkSubscription(block,targetsite)
      counter+=1
