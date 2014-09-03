#!/usr/bin/env python

import sys


class sessionModel(object):
    """ A generic virtual class which models the behaviour of a
    session type -- e.g. how people join 'rooms' for that session"""

    def __init__(self):
        """Initialisation"""
        print >> sys.stderr,"sessionModel is abstract and should", \
            "not be implemented"
        sys.exit()

    def addUser(self,u):
        """User arrives in stream"""

    def removeUser(self,u):
        """User removed from stream"""

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any stream model"""

    def getSessions(self):
        """ Return a list of lists of users in each stream"""

