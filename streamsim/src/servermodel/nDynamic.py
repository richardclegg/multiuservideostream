#!/usr/bin/env python


import serverModel
import sys
import random
from location.cluster import cluster
from location.datacentre import datacentre


class nDynamic(serverModel.serverModel):
    """ server model chooses n servers to be clustered"""

    def __init__ (self):
        """Initialise the nRandom server selection model"""
        self.noServers= 1
        self.updateInterval= 0
        self.lastUpdate= 0

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any server model"""
        try:
            self.noServers= int (js.pop("number"))
        except KeyError:
            pass
        except ValueError:
            print >> sys.stderr, "Number of servers specified in json for server model must be int"
            sys.exit()
        try:
            self.updateInterval= int (js.pop("update_interval"))
            self.lastUpdate= -self.updateInterval
        except KeyError:
            pass
        except ValueError:
            print >> sys.stderr, "Number of servers specified in json for server model must be int"
            sys.exit()
            
    @staticmethod
    def chooseServers( clusters, servers, qoeMod):
        """ Choose servers closest to several clusters """
        clusters.sort()
        clusters.reverse()
        centres= []
        
        slist=list(servers)
        #print "Getting best from ",len(clusters),"among",len(servers)
        for c in clusters:
            dc= c.getClosest(slist, qoeMod)
            #print "Returned",type(dc), dc.getLocation().lat,dc.getLocation().lon
            slist.remove(dc)
            centres.append(dc)
        return centres

    def updateServers(self,time,session, netMod, qoeMod, routeMod,demMod):
        """Given a session and a time update the server list for the session"""
        if session.changed == False:                    # Has anything changed
            return
        if time - self.lastUpdate < self.updateInterval:
            return
        choice= netMod.locations()                    # Look at all choices
        
        if (self.noServers == len(choice)):
            session.datacentres= choice
            return
        
        clusters= cluster.clusterUsers(session.getUsers(), self.noServers, qoeMod) 
        # choose enough servers
        centres= self.chooseServers(clusters,choice,qoeMod)
        session.datacentres= centres
            
            
        
        
