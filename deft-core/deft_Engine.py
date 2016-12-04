from pyutilib.component.config import *

import	pyutilib.workflow
from	pyutilib.workflow	import port
from	pyutilib.workflow	import TaskPlugin

import	networkx as nx
from	networkx.readwrite import json_graph

from	deft_Logger		import *
from	deft_Task		import DeftTaskPlugIn
from	deft_General_Utils	import *

from deft_Oracle_Utils	import deft_Oracle

#######################################################
class DeftEngine():
    """Constructor"""
    def __init__(self, directed_graph, logger = None):
        self.entry		= 0
        self.exit		= 0
        
        self.logger		= logger
        
        self.workflow		= None

        self.dg			= directed_graph

        self.nodes		= self.dg.nodes(data=True)
        self.edges		= self.dg.edges(data=True)
        self.N			= len(self.nodes)
        self.node_map		= {} # maps names to indices in the list - can be done differently, but it works

        if self.N==0: return
        
        
        sorted_nodes = nx.topological_sort(self.dg) # need the entry and exit points, and define special i/o: start and finish
        (self.entry, self.exit) = (sorted_nodes[0], sorted_nodes[len(sorted_nodes)-1])
        if self.logger: self.logger.info('Executing Meta-Task with entry point: '+self.entry)

        for n in range(self.N):
            node_name = self.nodes[n][0]
            node_data = self.nodes[n][1]
            state     = None
            try:
                state =  node_data['state']
            except:
                sys.exit(-2) # every task MUST have a state... FIXME later to handle gracefully

            # In order to populate the PyUtilib graph, create a task to be grafted onto a node

            task = pyutilib.workflow.TaskFactory('DeftTask', id=node_name, state=state, logger=self.logger)
            
            self.nodes[n]  = self.nodes[n] + (task,) # note that we are adding to a tuple this way
            self.node_map[node_name] = n


        self.nodes[self.node_map[self.entry]][2].set_input('start')
        self.nodes[self.node_map[self.exit]][2].set_output('finish')

        # Link the tasks, effectively creating a workflow. Supply info for PyUtilib Workflow - edge source, target, data.
        for e in self.edges: self.link_nodes(e)

        self.workflow = pyutilib.workflow.Workflow()		# Create a Workflow object
        self.workflow.add(self.nodes[self.node_map[self.exit]][2])	# Drop a single task into it, it will figure out dependencies automatically

    ###
    def check_workflow(self):
        for node in self.nodes:
            print 'node:', node

    ###
    def link_nodes(self, edge): # that helps with PyUtilib PW machinery
            name1	= edge[0]
            name2	= edge[1]
            edge_data	= edge[2]
            n1		= self.node_map[name1]
            n2		= self.node_map[name2]
    
            (ix, ox) = uni_name(name1,name2)
            
#            self.nodes[n1][2].set_output(ox, edge_data['state']) # note that we care about the state of the output (the edge)

            self.nodes[n1][2].set_output(ox, edge_data) # note that we care about the state of the output (the edge)
            self.nodes[n2][2].set_input(ix)

            self.nodes[n2][2].inputs[ix] = self.nodes[n1][2].outputs[ox] # the punchline! Here we connect the tasks

            # DEV self.nodes[n1][2].value_output(ox, edge_data['state']) # set it AFTER the connection is made


    ###
    def process(self, input):
        if self.workflow:
            result = self.workflow(start=input)	# Actuate the workflow
            if self.logger: self.logger.debug(3, 'Meta-Task output: '+str(result))


    ###
    # By now, the graph is processed. We need to harvest the status data
    # from the task objects and serialize it back into
    # plain node attributes, stored as a dictionary

    def harvest(self):
        for n in range(self.N):
            (node_name, node_data, node_task) = (self.nodes[n][0], self.nodes[n][1], self.nodes[n][2])
            try:
                s = node_task.get_state()    # print node_name, 'state!', s, node_data['comment']
                node_data['state'] = s
            except:
                pass

    ###
    def info(self):
        i = 'Meta: '+str(self.entry)
        nodes = self.dg.nodes()
        print nodes
        return i
#######################################################
class DeftTemplate():
    """Constructor"""
    def __init__(self, directed_graph, libref='', lib = False, file_seq = False, logger = None):
        self.dg			= directed_graph
        self.logger		= logger
        self.lib		= lib
        self.file_seq		= file_seq # how we generate serial numbers, if True than do the dumbed-down file-based test

        self.nodes		= self.dg.nodes(data=True)
        self.edges		= self.dg.edges(data=True)
        self.N			= len(self.nodes)
        self.E			= len(self.edges)

        tmpl_map = {} # for handling the templates, a map of "old" node labels to new ones
        
        sorted_nodes = nx.topological_sort(self.dg) # it's not 100% necessary, but it's more readable this way

        # Now we assign a "true" ID to the node, overwriting the template placeholder value
        if self.file_seq is True:
            print 'file serial' # this is now deprecated so we won't put new code in this branch as of 20131001
            for n in range(self.N):
                node_id = sorted_nodes[n]
                tmpl_map[node_id] = self.getSerial() # DEPRECATED!
        else:
            seqN = self.getSeq(self.N)
            for n in range(self.N):
                node_id = sorted_nodes[n]
                tmpl_map[node_id] = seqN[n]

        n1 = self.dg.nodes()

        nx.relabel_nodes(self.dg, tmpl_map, copy=False)
        
        n2 = self.dg.nodes()
        
        self.logger.info('Template substitution: '+str(n1)+str(n2))

        # This time, we need to grab the "entry" node, and use its ID as the name of the meta-task, which is to be added to all nodes and edges
    
        sorted_nodes = nx.topological_sort(self.dg)
        meta =  sorted_nodes[0]

        nodes = self.dg.nodes(data=True)

        # DISARM ALL IF MAKING A TASK FROM TEMPLATE, AND ADD LIBREF TO HEAD otherwise
        for n in range(self.N):
            (node_id, node_data) = (nodes[n][0], nodes[n][1])
            
            #            if node_id == meta:
            #                # print 'meta:', meta
            #                print libref,  ':', node_data['template']
            
            if libref!='':
                node_data['template'] = libref

            try:
                node_data['meta'] = meta # mark the meta-task, the parent, in each task
                if self.lib==True:
                    node_data['state'] = 'template'
                else:
                    node_data['state'] = 'disarmed'

            except:
                pass

        edges = self.dg.edges(data=True)

        seqE = self.getSeq(self.E)
        for n in range(self.E): # set the parent meta and get a proper sequential number
            (edge_source, edge_target, edge_data) = (edges[n][0], edges[n][1], edges[n][2])
            edge_data['meta'] = meta
            edge_data['id'] = seqE[n]

    ### Poor man's serial number generator, to be used only in basic testing
    def getSerial(self):
        f = open('serial.txt',"r")
        n = int(f.read()) + 1
        f.close()

        f = open('serial.txt',"w")
        f.write(str(n))
        f.close()
        return n
    
    ### Proper way: use the Oracle sequence
    def getSeq(self, cnt=1):
        d = deft_Oracle()
        return d.get_task_seq_db(cnt)


    def graph(self):
        return self.dg

# Comments:
# 1. edge_data['meta'] = meta # this works, too:  nx.set_edge_attributes(dg,'meta', {(edge_source, edge_target):meta})
