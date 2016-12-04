import	sys
import	logging
import json

from	pyutilib.component.config import *

import	pyutilib.workflow
from	pyutilib.workflow import port
from	pyutilib.workflow import TaskPlugin

#######################################################
class DeftTaskPlugIn(pyutilib.workflow.TaskPlugin):
    pyutilib.component.core.alias('DeftTask')
    """Constructor"""
    def __init__(self, id=None, name=None, meta=None, state=None, logger=None):
        if not name: name = id
        pyutilib.workflow.Task.__init__(self, name)
        self.state	= state
        self.id		= id
        self.name	= name
        self.state	= state
        self.logger	= logger

        ### This is a stub for the transition matrix, to be implemented later
        self.x_matrix = {'armed':'active'}

    ##### Simple wrappers for setting I/O of the task
    def set_input(self, input):
        self.inputs.declare(input) ### DEV self.inputs[input].set_value('test')
        if self.logger: self.logger.debug(5, '"'+sys._getframe().f_code.co_name+'":	Declared input '+input)

    ###
    def set_output(self, output, data={}):# default should only happen in the Exit node
        self.outputs.declare(output)		# PW method
        try:
            foo = data['state']
            if self.logger: self.logger.debug(5, '"'+sys._getframe().f_code.co_name+'":	Declared output '+output+' with state "'+foo+'"')
        except:
            if self.logger: self.logger.debug(5, '"'+sys._getframe().f_code.co_name+'":	Declared output '+output+' with no state')
            pass

        self.outputs[output].set_value(data)
#        print '!!!', self.outputs[output]

    ###
    def value_output(self, output, state='ready'):# default should only happen in the Exit node
        self.outputs[output].set_value(state)


    ##### Set/Get, for better readability
    def set_state(self, state):
        self.state = state
    ###
    def get_state(self):
        return self.state

    ####################################################################################################
    ####################################################################################################
    def execute(self):
        audit = 'Task ID: '+self.id+' Initial state: '+self.state+'	'

        state_before = self.state
        inputs_ready = True
        readiness    = {} # this is for logging purposes
        
        for k in sorted(self.inputs.keys()):
            data = self.inputs[k].value
            x = data['state']
            if x!='ready':
                inputs_ready=False
            if self.logger:
                if self.logger.debug_level >= 3:
                    readiness[k] = x

        audit += 'Inputs:	'+json.dumps(readiness)

        if inputs_ready and self.state=='armed': # this one line is the most important in DEFT
            self.state = 'active'

        state_after  = self.state
        

        for k in sorted(self.outputs.keys()):
            data = self.outputs[k].value
            if data == {}: data = {'state':'ready'}
            setattr(self, self.outputs[k].name, data)

        audit += ' Transition: '+state_before+'->'+state_after

        if self.logger: self.logger.debug(2, audit)

    ####################################################################################################
    ####################################################################################################
            
