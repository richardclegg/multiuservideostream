#!/usr/bin/env python


import serverModel
import sys
import random


class nRandom(serverModel.serverModel):
    """ server model chooses n servers from the list of servers at
    random -- uses them only"""

    def __init__ (self):
        """Initialise the nRandom server selection model"""
        self.noServers=1
        self.updateInterval=0
        self.lastUpdate=0

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any server model"""
        try:
            self.noServers= int (js.pop("number"))
        except KeyError:
            pass
        try:
            self.updateInterval= int (js.pop("update_interval"))
            self.lastUpdate= -self.updateInterval
        except KeyError:
            pass
        except ValueError:
            print >> sys.stderr, "Number of servers specified in json for server model must be int"
            sys.exit()



    def updateServers(self,time,session, netMod, qoeMod, routeMod, demMod):
        """Given a session and a time update the server list for the session"""
        if len(session.datacentres) > 0 and (self.updateInterval == 0 or 
            time - self.lastUpdate < self.updateInterval):
                return
        self.lastUpdate= time
        if session.changed == False:                    # Has anything changed
            return
        choice= netMod.locations()                    # Look at all choices
        if len(choice) <= self.noServers:
            session.datacentres= choice
            return
        # choose enough servers
        session.datacentres= random.sample(choice, self.noServers)
