#!/usr/bin/env python


import serverModel
import sys
import random
import location.location as location


class nStaticTime(serverModel.serverModel):
    """ server model chooses n servers to be clustered"""

    def __init__ (self):
        """Initialise the nRandom server selection model"""
        self.noServers= 1
        self.locMap= None
        self.serverMap= None

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any server model"""
        try:
            self.noServers= int (js.pop("number"))
        except KeyError:
            pass
        except ValueError:
            print >> sys.stderr, "Number of servers specified in json for server model must be int in file",fName
            sys.exit()
        try:
            filename= (js.pop("file"))
        except KeyError:
            print >> sys.stderr, "Must specify 'file' in JSON for nStatic server model", fName
            sys.exit()
        try:
            fptr= open(filename,'r')
        except IOError:
            print >> sys.stderr, "Cannot open",filename,"to read specified in",fName
            sys.exit()
        self.locMap={}
        while True:
            l= fptr.readline()
            if l == '':
                break
            #Skip comments and blank lines
            if l[0] == '\n' or l[0] == '#' or l[0] == '%':
                continue
            l=l.split('%')[0].split('#')[0] # strip comments
            parts= l.split(",")
            #Parse line by pairs
            if len(parts) %2 != 1:
                print >> sys.stderr, "Lines in ",filename,"read from JSON in",fName,"must be comma separated integer pairs begun with timezone"
                sys.exit()                
            locs=[]
            try:
                tz=int(parts[0])
            except ValueError:
                print >> sys.stderr, "First field in",filename,"read from JSON in",fName, 
                "must be integer"
                sys.exit()
            for i in range(1, len(parts),2):
                try:
                    lat= float(parts[i])
                    lon= float(parts[i+1])
                except ValueError:
                    print >> sys.stderr, "Lines in ",filename,"read from JSON in",fName,"must be comma separated pairs of floats"
                    print parts
                    sys.exit()
                locs.append(location.location(lat,lon))
            self.locMap[(tz,len(parts)/2)]= locs
            
        fptr.close()
                
           
    def createServerMap(self,netMod):
        """create a map from integer to selected servers"""
        self.serverMap={}
        for n in self.locMap:
            servers=[]
            for s in self.locMap[n]:
                serv=netMod.findServer(s)
                if serv == None:
                    print >> sys.stderr, "nStatic configuration in JSON contains lat long pair not corresponding to server"
                    sys.exit()
                servers.append(serv)
            self.serverMap[n]= servers
                
            

    def updateServers(self,time,session, netMod, qoeMod, routeMod,demMod):
        """Given a session and a time update the server list for the session"""
        if self.serverMap == None:
            self.createServerMap(netMod)
        tz= demMod.whichTime(time)
        session.datacentres= self.serverMap[(tz,self.noServers)]
