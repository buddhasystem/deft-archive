#!/usr/bin/env python
import sys
import argparse
import json

import logging

from pyutilib.component.config import *

import pyutilib.workflow
from pyutilib.workflow	import port
from pyutilib.workflow	import TaskPlugin

import networkx as nx
from networkx.readwrite import json_graph

import deft_General_Utils

from deft_Task		import DeftTaskPlugIn
from deft_Task		import map_nodes
from deft_General_Utils	import *
from deft_Oracle_Utils	import deft_Oracle

from deft_Graph_Schemas import *

from deft_Engine	import DeftEngine

def deft_log(debug, string):
    if debug > 0: logging.debug(string)


########################################################################################
#
#
#
#
#
#
#       DO NOT USE. THIS IS AN EARLY PROTOTYPE AND PROOF OF PRINCIPLE SCRIPT,
#       NO LONGER COMPATIBLE WITH OTHER MODULES IN THIS SUITE. USE DEFT-CLI INSTEAD.
#
#
#
#
#
#
#
########################################################################################

MODE = 'PROCESS' # default mode is to traverse DAG and perform transitions in the nodes

LOG_FILENAME = '/tmp/deft.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,filemode='w')

argParser = argparse.ArgumentParser()

# Generic options:
argParser.add_argument("-d", "--debug",		help="DEBUG level", default=0)

# GraphML parsing and serialization:
argParser.add_argument("-t", "--template",	help="Meta-Task Template input (GraphXML File)")
argParser.add_argument("-i", "--in_meta",	help="Meta-Task to be processed (GraphXML File)")
argParser.add_argument("-o", "--out_meta",	help="Processed Meta-Task (GraphXML File)")

# RDBMS options
argParser.add_argument("-p", "--purge",		help="Purge Meta-task from RDBMS, '0' means all, value must be given", default='')
argParser.add_argument("-s", "--store",		help="Store Meta-Task in RDBMS",  action='store_true', default='False')
argParser.add_argument("-r", "--retrieve",	help="Retrieve Meta-Task from RDBMS", default='')
argParser.add_argument("-f", "--fetch",		help="Single Task to be fetched", default='')

# Update state of task(s) and dataset(s)
argParser.add_argument("-T", "--update_task",	help="Update attributes of task(s)", default='')
argParser.add_argument("-D", "--update_dataset",help="Update attributes of dataset(s)", default='')

# Process (execute) task
argParser.add_argument("-x", "--execute",	help="Execute Meta-Task",  action='store_true', default='False')


args    = argParser.parse_args()
dg      = None # placeholder for the principal graph
debug   = 0
execute = args.execute


### Look at the arguments, log what we found, do a basic sanity check
if args.debug:
    debug = args.debug
    deft_log(debug, 'Debug level set to '+str(debug))

graph_source	= args.in_meta
graph_template	= args.template
graph_dest	= args.out_meta

########################## BASIC SANITY CHECK
if not graph_source and not graph_template and args.retrieve=='':
    logging.error("No template or input data specified, exiting...")
    sys.exit(-1)

if graph_source and graph_template:
    logging.error("Can't have both template and input task defined at the same time, exiting...")
    sys.exit(-1)

########################## END BASIC SANITY CHECK

    
########################## GENERIC MINOR DB OPERATIONS
if args.purge!='':
    if args.purge == '0':
        logging.info('DB purge request received for ALL Meta-Task: total deletion')
    else:
        logging.info('DB purge request received for Meta-Task '+args.purge)
        
    d = deft_Oracle()
    d.purge_meta_db(args.purge)
    logging.info('Task DB purged')
    sys.exit(0)

# Single Task
if args.fetch!='':
    logging.info('Fetch request received for task '+args.fetch)
    d = deft_Oracle()
    task = d.fetch_task_db(args.fetch)
    logging.info('Task '+ args.fetch +' fetched')
    print task # need to redirect to XML or DB
    sys.exit(0)
########################## END GENERIC MINOR DB OPERATIONS



########################## RETRIEVE FROM DB
if args.retrieve!='':
    logging.info('Retrieve request received for Meta-Task '+args.retrieve)

    d = deft_Oracle()
    meta = d.retrieve_meta_db(args.retrieve) # receive a tuple, see how's used below

    logging.info('Meta-Task '+ args.retrieve +' retrieved')

    dg = nx.DiGraph()

    # note that we have to stringify some data elements. Doing it in the Oracle
    # access method does not make it more elegant, unfortunately. Will change
    # eventually to automatic conversion TBD.

    for node in meta[0]:  # first element of the tuple is an array of nodes (tasks)
        nn = str(node[0]) # "node name"
        dg.add_node(nn)   # dgn = DeftGraphNode()  # yet to be developed
        
        nx.set_node_attributes(dg,'meta',	{nn:node[1]})
        nx.set_node_attributes(dg,'state',	{nn:node[2]})
        nx.set_node_attributes(dg,'tag',	{nn:node[3]})
        nx.set_node_attributes(dg,'comment',	{nn:node[4]})

    for edge in meta[1]: # second element of the tuple is an array of edges (datasets)
        edge_source = str(edge[3])
        edge_target = str(edge[4])
        
        dg.add_edge(edge_source, edge_target)
        
        et = (edge_source, edge_target)		# "edge tuple"
        nx.set_edge_attributes(dg,'id',		{et:edge[0]})
        nx.set_edge_attributes(dg,'meta', 	{et:edge[1]})
        nx.set_edge_attributes(dg,'state', 	{et:edge[2]})
        nx.set_edge_attributes(dg,'comment', 	{et:edge[5]})

        # artifact from an early prototype:        #    edges    = dg.edges(data=True)        #    nodes    = dg.nodes(data=True)

    if graph_dest:
        logging.info('Meta-Task '+ args.retrieve +' written to file '+graph_dest)
        nx.write_graphml(dg, graph_dest)

########################## END RETRIEVE FROM DB


########################## HANDLE TEMPLATES
if graph_template:
    MODE = 'TEMPLATE'			# replace task temporary IDs with serial numbers. Do not execute DAG.
    logging.debug('MODE set to TEMPLATE')
    dg = nx.read_graphml(graph_template)

    tmpl_map = {} # for handling the templates, a map of "old" node labels to new ones

    sorted_nodes = nx.topological_sort(dg) # it's not necessary to sort nodes for labeling purposes, but it's more readable this way
    for N in range(len(sorted_nodes)):
        node_name = sorted_nodes[N]
        tmpl_map[node_name] = deft_General_Utils.getSerial()

    n1 = dg.nodes()
    nx.relabel_nodes(dg, tmpl_map, copy=False)
    n2 = dg.nodes()
    logging.debug('Template substitution: '+str(n1)+str(n2))

    # this time, we need to make sure we grab the "entry" node, and use its ID as the name of the meta-task.
    # We'll need to substitute that into all nodes and edges
    
    sorted_nodes = nx.topological_sort(dg)
    meta =  sorted_nodes[0]

    nodes    = dg.nodes(data=True)
    for N in range(len(nodes)):
        (node_name, node_data) = (nodes[N][0], nodes[N][1])
        try: # print node_name, 'meta', node_data['meta']
            node_data['meta'] = meta
        except:
            pass

    edges = dg.edges(data=True)
    for N in range(len(edges)):
        (edge_source, edge_target, edge_data) = (edges[N][0], edges[N][1], edges[N][2])
        edge_data['meta'] = meta # this works, too:  nx.set_edge_attributes(dg,'meta', {(edge_source, edge_target):meta})

    if graph_dest:
        nx.write_graphml(dg, graph_dest)
    sys.exit(0)
########################## END TEMPLATE BLOCK


########################## READ GRAPHML
if graph_source:
    logging.debug('Reading Meta-Task from source file ' + graph_source)
    dg = nx.read_graphml(graph_source)
########################## END READ GRAPHML BLOCK


########################## UPDATE TASK
task_update = {}
if args.update_task!='':
    task_update = json.loads(args.update_task)
    for t in task_update:
        task_id = t.keys()[0]
        for k in t[task_id].keys():
            print task_id, k, t[task_id][k]
            dg.node[task_id][k] = t[task_id][k]
            
    if graph_dest:
        nx.write_graphml(dg, graph_dest)
    sys.exit(0)
########################## END UPDATE TASK


########################## EXECUTE
if execute is True:
    print 'EXECUTION\n', execute
    E = DeftEngine(dg, '2000')
    print E.info()
    E.process('ready')
    E.harvest()

    if graph_dest:
        nx.write_graphml(dg, graph_dest)
    sys.exit(0) # to be changed, this is a dev plug
########################## END EXECUTE


########################## DB STORE
if args.store==True:
    # store the meta-task and its constituent tasks
    logging.info('DB task store request received')

    tasks = []
    for N in range(len(nodes)):
        t = {}
        (node_name, node_data, node_task) = (nodes[N][0], nodes[N][1], nodes[N][2])
        t['TASK_ID']		= node_name
        t['TASK_META']		= node_data['meta']
        t['TASK_TAG']		= node_data['tag']
        t['TASK_STATE']		= node_data['state']
        t['TASK_COMMENT']	= node_data['comment']
        tasks.append(t)

    datasets = []
    for N in range(len(edges)):
        d = {}
        (edge_source, edge_target, edge_data) = (edges[N][0], edges[N][1], edges[N][2])
        d['DATASET_ID']		= edge_data['id']
        d['DATASET_META']	= edge_data['meta']
        d['DATASET_SOURCE']	= edge_source
        d['DATASET_TARGET']	= edge_target
        d['DATASET_STATE']	= edge_data['state']
        d['DATASET_COMMENT']	= edge_data['comment']
        datasets.append(d)

    db = deft_Oracle()
    print 'inserting tasks'
    db.insert_task_db(tasks)
    print 'inserting datasets'
    db.insert_dataset_db(datasets)

    sys.exit(0)
########################## END DB STORE


### ARCHIVE
# Previously used in GraphML parsing block of code

#    # load the data from the graph!
#    edges    = dg.edges(data=True)
#    nodes    = dg.nodes(data=True)
#    node_map = {} # a dictionary with values containing a list: the node name, node data and the PW task object

#    for N in range(len(nodes)):
#        node_name = nodes[N][0]
#        node_data = nodes[N][1]
#        state     = None

#        try:
#            state =  node_data['state']
#        except:
#            sys.exit(-2) # every task MUST have a state

#        task = pyutilib.workflow.TaskFactory('DeftTask', id=node_name, state=state, debug=debug) # create a task to be grafted onto a node
#        nodes[N]  = nodes[N] + (task,) # note that we are adding to a tuple this way

#        node_map[node_name] = N
        
#    ### end loop: for N in range


# Previously used in templates
#    for N in range(len(nodes)):
#        node_name = nodes[N][0]
#        node_data = nodes[N][1]
#        state     = None
#        try:
#            state =  node_data['state']
#        except:
#            sys.exit(-2) # every task MUST have a state
#    ### end loop: for N in range

#    # For them, define special i/o points: start and finish, which are not in the graph, but implied
#    (graph_entry, graph_exit) = (sorted_nodes[0], sorted_nodes[len(sorted_nodes)-1])


#leftovers from execute
#     nodes = dg.nodes(data=True)
#     edges = dg.edges(data=True)

#     (nodes, node_map)  = map_nodes(nodes, debug) # augments each node with the task object and maps nodes to serial intra-graph indices
    
#     sorted_nodes = nx.topological_sort(dg) # need to get entry and exit points, for them, define special i/o points: start and finish
#     (graph_entry, graph_exit) = (sorted_nodes[0], sorted_nodes[len(sorted_nodes)-1])

#     nodes[node_map[graph_entry]][2].set_input('start')
#     nodes[node_map[graph_exit]][2].set_output('finish')

#     for e in edges: link_nodes(nodes, node_map, e[0], e[1], e[2]) # that's for PyUtilib Workflow - edge source, target, data

#     w = pyutilib.workflow.Workflow()		# Create a Workflow object
#     w.add(nodes[node_map[graph_exit]][2])	# Drop a single task into it, it will figure out dependencies automatically

#     p = w(start='ready')			# Finally, actuate the workflow

#     # By now, the graph is processed. We need to harvest the status data
#     # from the task objects and serialize it back into
#     # plain node attributes, stored as a dictionary

#     for N in range(len(nodes)):

#         (node_name, node_data, node_task) = (nodes[N][0], nodes[N][1], nodes[N][2])
    
#         try:
#             s = node_task.get_state()    # print node_name, 'state!', s, node_data['comment']
#             node_data['state'] = s
#         except:
#             pass

