#!/usr/bin/env python

import sys


class routeModel(object):
    """ A generic model for route choice in the network
    this is not instantiated but is the base class for
    actual route models"""

    def __init__(self):
        """ Initialise base class for route model"""


    def parseJSON(self,js,fName):
        """  parse JSON associated with this routeModel"""
        print >> sys.stderr,"routeModel is abstract and should", \
            "not be implemented"
        raise NotImplementedError("routeModel is abstract")

    def getRoute(self, servers, start, end, qoeModel):
        """Return a route from start to end via servers
            given a particular QoE model"""

    def symmetric(self):
        """ Is the route for this model symmetric"""
        return True
