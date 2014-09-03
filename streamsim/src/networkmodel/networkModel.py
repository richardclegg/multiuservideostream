#!/usr/bin/env python

import sys


class networkModel(object):
    """ A generic virtual class which models the behaviour of a
    a networkModel e.g costs and locations"""

    def __init__(self):
        """Initialisation"""


    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any network model"""
        print >> sys.stderr,"networkModel is abstract and should", \
            "not be implemented"
        raise NotImplementedError("networkModel is abstract")

    def locations(self):
        """ return a list of locations where this network has nodes"""
        return []

    def price(self,route, fullstream, partstream, timedelta):
        """ return the price as a tuple for following a tuple of locations, e.g.
         (0,1,3) is price for entering network at 0, going to 1
         then exiting at 3 price is a tuple of 
         host->net net->net net->host cpu"""
        return (0.0,0.0,0.0,0.0)
        
    def findServer(self,location):
        """ Return the datacentre object which is at a given location"""
        
        for l in self.locations():
            if abs(l.getLocation().lat - location.getLocation().lat) < 0.001 \
                and abs(l.getLocation().lon - location.getLocation().lon) < 0.001:
                return l
        return None
    
    def getCostTuple(self, session, routeModel,timedelta, routeMod):
        """ Return a 4-tuple of costs for a session following a given
        route model -- tuple is host->net net->net net->host cpu"""
        """ Return a 4-tuple of costs for a session following a given
        route model -- tuple is host->net net->net net->host cpu"""

        return (0.0,0.0,0.0,0.0)
