from deft_Logger	import *
from deft_Oracle_Utils	import deft_Oracle

import networkx as nx
from networkx.readwrite import json_graph
from deft_Graph_Schemas import *

# temp - for testing
import datetime
from datetime import datetime


########################################################################################
# WARNING: currently this method is out of sync, needs an update
def oracle2graph(meta, db, logger=None):
    if logger: logger.info('Retrieve request received for Meta-Task '+meta)

    data = None
    
    try:
        data = db.retrieve_meta_db(meta) # receive a tuple, see how's used below
    except:
        if logger: logger.error('Catastrophic error during retrival of Meta-Task '+meta)
        return None

    if logger: logger.info('Meta-Task '+ meta +' retrieved')

    dg = nx.DiGraph()

    # note that we have to stringify some data elements. Doing it in the Oracle
    # access method does not make it more elegant, unfortunately. Will change
    # eventually to automatic conversion TBD.
    
    print data[0]
    for node in data[0]:  # first element of the tuple is an array of nodes (tasks)
        nn = str(node[0]) # "node name"
        dg.add_node(nn)   # dgn = DeftGraphNode()  # yet to be developed
        
        nx.set_node_attributes(dg,'meta',	{nn:node[1]})
        nx.set_node_attributes(dg,'state',	{nn:node[2]})
        nx.set_node_attributes(dg,'tag',	{nn:node[3]})
        nx.set_node_attributes(dg,'comment',	{nn:node[4]})

    for edge in data[1]: # second element of the tuple is an array of edges (datasets)
        edge_source = str(edge[3])
        edge_target = str(edge[4])
        
        dg.add_edge(edge_source, edge_target)
        
        et = (edge_source, edge_target)		# "edge tuple"
        nx.set_edge_attributes(dg,'id',		{et:edge[0]})
        nx.set_edge_attributes(dg,'meta', 	{et:edge[1]})
        nx.set_edge_attributes(dg,'state', 	{et:edge[2]})
        nx.set_edge_attributes(dg,'comment', 	{et:edge[5]})

        # artifact from an early prototype:  edges = dg.edges(data=True), nodes = dg.nodes(data=True)

    return dg
########################################################################################
def graph2oracle(graph, db, logger=None):
    sorted_nodes = nx.topological_sort(graph)
    entry = str(sorted_nodes[0])

    if(logger):
        logger.info('Store request received for Meta-Task '+entry)

    nodes = graph.nodes(data=True)
    edges = graph.edges(data=True)

    tasks = []
    meta  = {}


    # Will need to think through int vs str content as the node name... For now just convert:
    for N in range(len(nodes)):
        t = {}
        (node_name, node_data) = (str(nodes[N][0]), nodes[N][1])
        t['TASK_ID']		= int(node_name)
        t['TASK_NAME']		= str(node_data['name'])
        t['TASK_META']		= int(node_data['meta'])
        t['TASK_STATE']		= str(node_data['state'])
        t['TASK_COMMENT']	= str(node_data['comment'])
        t['TASK_TAG']		= str(node_data['tag'])
        t['TASK_PARAM']		= str(node_data['param'])
        t['TASK_CLOUD']		= str(node_data['cloud'])
        t['TASK_SITE']		= str(node_data['site'])
        t['TASK_VO']		= str(node_data['vo'])
        t['TASK_TRANSUSES']	= str(node_data['transuses'])
        t['TASK_TRANSHOME']	= str(node_data['transhome'])
        t['TASK_TRANSPATH']	= str(node_data['transpath'])
        t['TASK_PROCESSINGTYPE']= str(node_data['processingtype'])
        t['TASK_TASKTYPE']	= str(node_data['tasktype'])
        t['TASK_PRODSOURCELABEL']= str(node_data['prodsourcelabel'])
        t['TASK_CORECOUNT']	= int(node_data['corecount'])
        t['TASK_RUNNUM']	= int(node_data['runnum'])
        t['TASK_TRANSPATH']	= str(node_data['transpath'])
        t['TASK_USERNAME']	= str(node_data['username'])
        t['TASK_WORKINGGROUP']	= str(node_data['wg'])
        t['TASK_ISSUE']		= str(node_data['issue'])
        tasks.append(t)
            
        if node_name==entry:  # the entry node fills both the meta task and the individual entry task
            meta['META_ID'] =		int(entry)
            meta['META_NAME'] =		str(node_data['name'])
            meta['META_TEMPLATE'] =	str(node_data['template'])
            meta['META_REQUESTOR'] =	str(node_data['requestor'])
            meta['META_MANAGER'] =	str(node_data['manager'])
            meta['META_COMMENT'] =	str(node_data['comment'])
            meta['META_STATE'] =	str(node_data['state'])
            meta['META_VO'] =		str(node_data['vo'])
            meta['META_WORKINGGROUP'] =	str(node_data['wg'])
            meta['META_PRODSOURCELABEL']= str(node_data['prodsourcelabel'])
            meta['META_CLOUD'] =	str(node_data['cloud'])
            meta['META_SITE'] =		str(node_data['site'])
            meta['META_ISSUE']		= str(node_data['issue'])

    datasets = []
    for N in range(len(edges)):
        d = {}
        (edge_source, edge_target, edge_data) = (edges[N][0], edges[N][1], edges[N][2])
        d['DATASET_ID']		= int(edge_data['id'])
        d['DATASET_NAME']	= str(edge_data['name'])
        d['DATASET_META']	= str(edge_data['meta'])
        d['DATASET_SOURCE']	= int(edge_source)
        d['DATASET_TARGET']	= int(edge_target)
        d['DATASET_STATE']	= str(edge_data['state'])
        d['DATASET_COMMENT']	= str(edge_data['comment'])
        d['DATASET_FLAVOR']	= str(edge_data['flavor'])
        d['DATASET_FORMAT']	= str(edge_data['format'])
        d['DATASET_TOKEN']	= str(edge_data['token'])
        d['DATASET_OFFSET']	= int(edge_data['offset'])
        datasets.append(d)

    if logger: logger.debug(1, 'Attempt to insert Meta-Task '+entry)
    try:
        db.insert_meta_db(meta)
    except:
        if logger: logger.error('Inserting Meta-Task '+entry+' failed')

    try:
        db.insert_task_db(tasks)
    except:
        if logger: logger.error('Inserting tasks for Meta-Task '+entry+' failed')

    if logger: logger.debug(1, 'Attempt to insert datasets for Meta-Task '+entry)

    try:
        db.insert_dataset_db(datasets)
    except:
        if logger: logger.error('Inserting datasets for Meta-Task '+entry+' failed')

########################################################################################
# Strictly for debugging - validation of the insert operation for tasks, to double check
# on columns names, formats, etc.
def graph2oracle_test(graph, db, logger=None):
    tasks = []
    t = {
        'TASK_ID': 9999,
        'TASK_NAME': 'DEFT',
        'TASK_META': 9999,
        'TASK_USERNAME': 'p',
        'TASK_WORKINGGROUP': 'AP',
        'TASK_MODIFICATIONTIME': datetime(2013, 11, 30, 3, 28, 17),
        'TASK_CLOUD': 'CERN',
        'TASK_SITE': 'test',                                                 
        'TASK_STATE': 'template',
        'TASK_PARAM': 'entry',
        'TASK_TAG': 'entry',
        'TASK_COMMENT': 'Using ADCR',
        'TASK_VO': 'atlas',                  
        'TASK_TRANSUSES': ' 1',                                                   
        'TASK_TRANSHOME': ' 1',                                                
        'TASK_TRANSPATH': ' 1',                                                
        'TASK_PROCESSINGTYPE': ' 1',
        'TASK_TASKTYPE': ' 1',                                           
        'TASK_PRODSOURCELABEL': 'managed',
        'TASK_CORECOUNT': 0,                                    
        'TASK_RUNNUM': 0,                                                  
        'TASK_ISSUE': 'PRODSYS-72'
        }
    tasks.append(t)
    try:
        db.insert_task_db(tasks)
    except:
        print 'fail'
