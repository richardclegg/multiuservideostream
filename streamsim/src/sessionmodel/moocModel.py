#!/usr/bin/env python

import random
import sys

import sessionModel
import session

class moocModel (sessionModel.sessionModel):
    """mood model is a session where everyone is in the same
    chat"""

    def __init__(self):
        """Initialise the poker model"""
        self.session= session.session(1)
        self.changed=True
        self.datacentres= []
        

    def addUser(self,u):
        """User arrives in stream"""
        self.session.addUser(u)
        self.changed=True


    def removeUser(self,u):
        """User removed from session"""
        self.session.delUser(u)
        self.changed= True

    def getSessions(self):
        """ Return a list where each element is a list of sessions"""
        return [self.session]

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName"""
       
