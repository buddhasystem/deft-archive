import logging

#################################################################################
class DeftLogger():
    """Constructor"""
    def __init__(self, filename='/tmp/deft.log', debug = 1000):
        logging.basicConfig(filename=filename,level=logging.DEBUG,filemode='w')
        self.debug_level = debug

    ###
    def debug(self, debug_level, string):
        if self.debug_level >= debug_level: logging.debug(string)

    ###
    def error(self, string):
        logging.error(string)

    ###
    def info(self, string):
        logging.info(string)
