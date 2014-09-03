#!/usr/bin/env python

import sys

class serverModel(object):
    """ A base class model which reads in a list of servers, costs
    and chooses which servers to use"""


    def __init__(self):
        """Initialise function for base class server Model
        this is a virtual class which should not be
        initialised"""
        print >> sys.stderr,"serverModel is abstract and should", \
            "not be implemented"
        sys.exit()

    def setup(self):
        """ Initialisation for basic tasks which all server models
            undertake"""
        self.noServers= 1    #Number of live servers
        self.serverList=None  #All potential servers

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any server model"""



    def updateServers(self,time,session, netMod, qoeMod,routeMod,demMod):
        """Given a session and a time update the server list for the session"""

