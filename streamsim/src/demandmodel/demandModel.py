#!/usr/bin/env python

import sys


class demandModel(object):
    """ A base class demand Model to produce arrivals and
    departures"""


    def __init__(self):
        """Initialise function for base class demand Model
        this is a virtual class which should not be
        initialised"""
        print >> sys.stderr,"streamModel is abstract and should", \
            "not be implemented"
        sys.exit()

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any demand model"""


    def nextArrival(self, time):
        """ return an object of type user"""

        return(None)
