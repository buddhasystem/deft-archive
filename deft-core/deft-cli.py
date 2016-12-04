#!/usr/bin/env python
import sys
import argparse
import json

from pyutilib.component.config import *

import pyutilib.workflow
from pyutilib.workflow	import port
from pyutilib.workflow	import TaskPlugin

import networkx as nx
from networkx.readwrite import json_graph

import deft_General_Utils

from deft_Task		import DeftTaskPlugIn

from deft_General_Utils	import *
from deft_Logger	import *
from deft_Oracle_Utils	import deft_Oracle

from deft_Graph_Schemas import *
from deft_Graph_Oracle_Adaptor import *

from deft_Engine	import DeftEngine
from deft_Engine	import DeftTemplate


########################################################################################
########################################################################################
########################################################################################

MODE = 'PROCESS' # default mode is to traverse DAG and perform transitions in the nodes

argParser = argparse.ArgumentParser()

# Generic options:
argParser.add_argument("-d", "--debug",		help="DEBUG level", default=1000)

# GraphML parsing and serialization:
argParser.add_argument("-t", "--template",	help="Meta-Task Template input (GraphXML File)")
argParser.add_argument("-i", "--in_meta",	help="Meta-Task to be processed (GraphXML File)")
argParser.add_argument("-o", "--out_meta",	help="Processed Meta-Task (GraphXML File)")

# RDBMS options
argParser.add_argument("-S", "--simu",		help="Simulate RDBMS read/write operations without executing them",  action='store_true', default='False')
argParser.add_argument("-p", "--purge",		help="Purge Meta-task from RDBMS, '0' means all, value must be given", default='')
argParser.add_argument("-s", "--store",		help="Store Meta-Task in RDBMS",  action='store_true', default='False')
argParser.add_argument("-l", "--lib",		help="Store Template in library, in RDBMS",  action='store_true', default='False')
argParser.add_argument("-L", "--libref",	help="Template reference number for task (advanced, deprecated)", default='')
argParser.add_argument("-r", "--retrieve",	help="Retrieve Meta-Task from RDBMS", default='')
argParser.add_argument("-f", "--fetch",		help="Single Task to be fetched", default='')
argParser.add_argument("-c", "--comm",		help="Update comm table", default='')

# Update state of task(s) and dataset(s)
argParser.add_argument("-T", "--update_task",	help="Update attributes of task(s)", default='')
argParser.add_argument("-D", "--update_dataset",help="Update attributes of dataset(s)", default='')

# Process (execute) task
argParser.add_argument("-x", "--execute",	help="Execute Meta-Task",  action='store_true', default='False')

# Repeat N times (for benchmarking and testing)
argParser.add_argument("-N", "--repeat",	help="Repeat action N times", default=1, dest='N')

# Defalt task parameters, for testing (JSON in current design)
argParser.add_argument("-P", "--task_param",	help="Default Task Parameters")

# Get a serial number using DB sequence (oracle)
argParser.add_argument("-Q", "--file_seq",		help="Get File-based Sequence for Task number (deprecated)",  action='store_true', default='False', dest='file_seq')

##############################################
args    = argParser.parse_args()

# print args.task_param
# sys.exit(-1)

dg      = None # placeholder for the principal graph
debug_level   = 1000 # a large number so no debugged messages are logged by default
execute = args.execute

###
if args.comm != '':
    comm_message = json.loads(args.comm)
    for k in comm_message.keys():
        print k, comm_message[k]

    d = deft_Oracle()
    d.update_comm(comm_message)
    sys.exit(-1)


###
if args.debug:
    debug_level = int(args.debug)

### Start the logging
logger = DeftLogger(filename = '/tmp/deft.log', debug = debug_level)

logger.debug(1, "Debug level set to "+str(debug_level))

### Look at the arguments, log what we found, do a basic sanity check

graph_source	= args.in_meta
graph_template	= args.template
graph_dest	= args.out_meta

########################## BASIC SANITY CHECK
if not graph_source and not graph_template and args.retrieve=='' and args.purge=='':
    logger.error("No template or input data specified, exiting...")
    sys.exit(-1)

if graph_source and graph_template:
    logger.error("Can't have both template and input task defined at the same time, exiting...")
    sys.exit(-1)
    
########################## GENERIC MINOR DB OPERATIONS
if args.purge!='':
    if args.purge == '0':
        logger.info('DB purge request received for ALL Meta-Task: total deletion')
    else:
        logger.info('DB purge request received for Meta-Task '+args.purge)
        
    d = deft_Oracle(args.simu)
    d.purge_meta_db(args.purge)
    logger.info('Task DB purged')
    sys.exit(0)

# Single Task
if args.fetch!='':
    logger.info('Fetch request received for task '+args.fetch)
    d = deft_Oracle()
    task = d.fetch_task_db(args.fetch)
    logger.info('Task '+ args.fetch +' fetched')
    print task # need to redirect to XML or DB
    sys.exit(0)

########################## READ THE META-TASK FROM THE SPECIFIED SOURCE
########################## 
########################## A) RETRIEVE FROM DB
if args.retrieve!='':
    d = deft_Oracle(args.simu)
    dg = oracle2graph(args.retrieve, d, logger = logger)

########################## B) HANDLE TEMPLATES
if graph_template:
    logger.info('Reading Meta-Task from template file ' + graph_template)
    template = nx.read_graphml(graph_template)
    
    # that should result in a ready to use meta-task, or of the "lib" option was
    # chosen, in a template entry
    T  = DeftTemplate(template, libref=args.libref, lib=args.lib, file_seq=args.file_seq, logger=logger)
    dg = T.graph()

########################## C) READ PREFAB GRAPHML
if graph_source:
    logger.info('Reading Meta-Task from source file ' + graph_source)
    dg = nx.read_graphml(graph_source)

########################## UPDATE THE META-TASK
########################## 
########################## A) UPDATE BASED ON JSON STRING
task_update = {}
if args.update_task!='':
    task_update = json.loads(args.update_task)
    for t in task_update:
        task_id = t.keys()[0]
        for k in t[task_id].keys():
            print task_id, k, t[task_id][k]
            dg.node[task_id][k] = t[task_id][k]
            
########################## EXECUTE
if execute is True:
    for i in range(int(args.N)):
        logger.debug(1, "Repetition number "+str(i+1))
        E = DeftEngine(dg, logger)
        starter_dataset = {'state':'ready'}
        E.process(starter_dataset)
        E.harvest()

########################## PERSIST THE META-TASK:
##########################
########################## DB STORE
if args.store==True or args.lib==True:
    # store the meta-task and its constituent tasks, or deposit the template into the table, in the "template" status

    d = deft_Oracle(args.simu)
    graph2oracle(dg, d, logger)

########################## SERIALIZE TO XML - catch all
if graph_dest:
    nx.write_graphml(dg, graph_dest)

########################## TA-DUH!
sys.exit(0)

