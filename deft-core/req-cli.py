#!/usr/bin/env python
import sys
import argparse
import json

from deft_Oracle_Utils	import deft_Oracle

###
argParser = argparse.ArgumentParser()

argParser.add_argument("-r", "--req", help="request", default='')
args = argParser.parse_args()

req = json.loads(args.req)
for k in req.keys():
    print k, req[k]

d = deft_Oracle()
try:
    d.update_req(req)
    sys.exit(0)
except:
    print 'failed to update request'
    sys.exit(-1)
