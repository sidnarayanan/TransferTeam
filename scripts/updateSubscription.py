#!/usr/bin/env python

import os
import pycurl
import urllib
from optparse import OptionParser

debug=True
#debug=False

def updateSubscription(block, node, priority):
    proxyfile='/tmp/x509up_u'+str(os.getuid())
    cadir='/etc/grid-security/certificates'

    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO,proxyfile)
    c.setopt(pycurl.CAPATH,cadir)
    c.setopt(pycurl.SSLKEY,proxyfile)
    c.setopt(pycurl.SSLCERT,proxyfile)
    
    url='https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&block=' + block.replace('#','%23',1) + '&node=' + node + '&priority=' + priority
    #url='https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&block=' + block.replace('#','%23',1) + '&node=' + node + '&suspend_until=' + priority
    print url,pycurl.URL 
    #if debug == True : print url,pycurl.URL 
 
    c.setopt(pycurl.URL, url)
    post_data = {'block': block , 'node': node , 'priority': priority}
    #post_data = {'block': block , 'node': node , 'suspend_until': priority}

    postfields = urllib.urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

def updateSubscriptionDS(dataset, node, priority):
    proxyfile='/tmp/x509up_u'+str(os.getuid())
    cadir='/etc/grid-security/certificates'

    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO,proxyfile)
    c.setopt(pycurl.CAPATH,cadir)
    c.setopt(pycurl.SSLKEY,proxyfile)
    c.setopt(pycurl.SSLCERT,proxyfile)
    
    url='https://cmsweb.cern.ch/phedex/datasvc/perl/prod/updatesubscription?nocache=1&dataset=' + dataset + '&node=' + node + '&priority=' + priority
    print url,pycurl.URL 
 
    c.setopt(pycurl.URL, url)
    post_data = {'dataset': dataset , 'node': node , 'priority': priority}

    postfields = urllib.urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()

if __name__ == '__main__':
  usage  = "Usage: %prog --block <block> --node <node> --priority <low,normal,high>"
  parser = OptionParser(usage=usage)
  parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
  parser.add_option("-b", "--block", action="store", type="string", default=None, dest="block", help="Block Name")
  parser.add_option("-d", "--dataset", action="store", type="string", default=None, dest="dataset", help="Dataset Name")
  parser.add_option("-n", "--node", action="store", type="string", default=None, dest="node", help="Node Name")
  parser.add_option("-p", "--priority", action="store", type="string", default=None, dest="priority", help="Priority")

  (opts, args) = parser.parse_args()

  if ((opts.block == None and opts.dataset == None) or opts.node == None or opts.priority == None):
      parser.error("Define block, node and priority")

  dataset = opts.dataset
  block = opts.block
  node = opts.node
  priority = opts.priority
  debug = opts.verbose

  if block:
    result = updateSubscription(block, node, priority)
  else:
    result = updateSubscriptionDS(dataset, node, priority)
