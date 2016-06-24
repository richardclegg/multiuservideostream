#!/usr/bin/env python

import sys

import networkModel
import location.datacentre as datacentre
import location.location as location


class instanceCostNetwork (networkModel.networkModel):
    """ A generic virtual class which models the behaviour of a
    a networkModel e.g costs and locations"""

    def __init__(self):
        """Initialisation"""
        self.betweenCost= 0.0   #Cost per MB between data centres
        self.fullStream= 1.0    #Bandwidth of full_stream in MB
        self.compressedStream=0.2    #Bandwidth of compressed_stream
        self.usersPerInstance=100 #Users per instance

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any stream model"""
        
        try:
            netFName= js.pop("file")
        except ValueError:
            print >> sys.stderr,"JSON for instanceCostNetwork must",\
                'contain "file" with filename of network description in', \
                    fName
            raise ValueError
        try:
            self.betweenCost= float(js.pop("between_cost_dollar_GB"))

        except:
            print >> sys.stderr,"JSON for instanceCostNetwork must",\
                'contain "between_cost_dollar_GB" -- cost of transfer', \
                ' between data centres as float in',fName
            raise ValueError
        try:
            self.fullStream= float(js.pop("full_stream_MBs"))
        except ValueError:
            print >> sys.stderr,"JSON for instanceCostNetwork must",\
                'contain cost per MB/s as float "full_stream_MBs"'
            raise ValueError
        try:
            self.compressedStream= float(js.pop("compressed_stream_MBs"))
        except ValueError:
            print >> sys.stderr,"JSON for instanceCostNetwork must",\
                'contain compressed stream rate MB/s as float', \
                '"compressed_stream_MBs"'
            raise ValueError
        try:
            self.usersPerInstance= int(js.pop("users_per_instance"))
        except ValueError:
            print >> sys.stderr,"JSON for instanceCostNetwork must",\
                'contain nnumber of users per instance as int', \
                '"users_per_instance"'
            raise ValueError            
        self.parseInstCostFile(netFName,fName)

    def parseInstCostFile(self,netFName,fName):
        """ Read the network file that contains locations and prices"""
        try:
            f= open(netFName)
        except IOError:
            print >> sys.stderr, "Unable to open network_model file", \
                netFName,"defined in JSON",fName
            sys.exit()
        self.nodes=[]
        while True:
            origline= f.readline()
            if origline == '':
                break
            #Skip blank lines and comments
            if origline[0] == '\n' or origline[0] == '#' or origline[0] == '%':
                continue
            l=origline.split('%')[0].split('#')[0] # strip comments
            parts= l.split(",")
            if len(parts) != 4 and len(parts) != 5:
                print >> sys.stderr,"Lines in instanceCostNetwork file", \
                    netFName,' are expected to be 5 tuple floats or ', \
                    ' 6 tuple with zone string as third arg', \
                    'specified in JSON',fName
                print >> sys.stderr,'Line',origline
                raise ValueError
            try:
                loc= (float(parts[0]),float(parts[1]))
                if len(parts) == 6:
                    zone= parts[2]
                    incost= float(parts[3])
                    outcost= float(parts[4])
                    instcost= float(parts[5])
                else:
                    zone=None
                    incost= float(parts[2])
                    outcost= float(parts[3])
                    instcost= float(parts[4])
            except:
                print >> sys.stderr,"Lines in instanceCostNetwork file", \
                    netFName,' are expect to have loc then in, out and ',\
                    'instcost in ',fName
                print >> sys.stderr,'Line',origline
                raise ValueError
            if loc[0] < -90 or loc[0] > 90 or loc[1] < -180 or \
                loc[1] > 180:
                print >> sys.stderr,"Lat, long must be in ranges", \
                    '[-90,90],[-180,180] respectively in',netFName, \
                    'referenced from JSON',fName
                raise ValueError
            if incost < 0 or outcost < 0 or instcost < 0:
                print >> sys.stderr,'Specified costs must be +ve'\
                     'in',netFName, 'referenced from JSON',fName
                print >> sys.stderr,'line',origline
                print >> sys.stderr,'parts',parts
                raise ValueError
            self.nodes.append(datacentre.datacentre( \
                location.location(loc[0],loc[1],zone), \
                incost,outcost,instcost))
        f.close()

    def locations(self):
        """ return a list of locations where this network has nodes"""
        return self.nodes

    def getCostTuple(self, session, timedelta, routeMod):
        """ Return a 4-list of costs for a session following a given
        route model -- tuple is host->net net->net net->host cpu"""
        
        costs= session.getCosts()
        if costs == None:
            host2net= 0.0
            net2net=0.0
            net2host=0.0
            # part stream is what is normally sent on this route between this
            #user pair only -- averaged
            # 1/noUsers of time it is full stream
            # (noUsers-1)/noUsers of time it is compressed Stream
            noUsers= session.noUsers()
            if noUsers <= 1:
                costs= [0.0,0.0,0.0,0.0]
                session.setCosts(costs)
                return costs
            partStream= self.fullStream/noUsers+self.compressedStream* \
                (noUsers-1)/noUsers
            # Data is only sent once between a pair of routers
            # and once between a user and a router 
            rdict={}  # Dictionary of links between routers
            indict={}  # Dictionary of links from server to router.
            for r in session.getRoutes():
				# If we never saw r[0]--r[1] add inbound cost
                if not indict.has_key((r[0],r[1])):
                    indict[(r[0],r[1])]= True
                    host2net+= r[1].inCost*self.fullStream
                # Add route out bound cost
                net2host+= r[-2].outCost*partStream
                
                # If routing is symmetric this route counts for
                # both directions -- so also add return costs
                # in same way
                if routeMod.symmetric():
					net2host+= r[1].outCost*partStream
					if not indict.has_key((r[-1],r[-2])):
						indict[(r[-1],r[-2])]= True
						host2net+= r[-2].inCost*self.fullStream                
					
                if len(r) > 3:
                    for i in range(1,len(r)-2):
                        if not rdict.has_key((r[0],r[i],r[i+1])):
                            rdict[(r[0],r[i],r[i+1])]= True
                            net2net+=self.betweenCost*partStream
                            if routeMod.symmetric():
								rdict[(r[-1],r[i+1],r[i])]= True
								net2net+=self.betweenCost*partStream
            #1000 factor because data transfer in MB/s costs in GB
            # No CPU costs in this setting
            costs=[host2net/1000,net2net/1000,net2host/1000,0.0]
            session.setCosts(costs)
        outcosts= list(costs)
        for i in range(len(outcosts)):
                outcosts[i]*= timedelta
        return outcosts

        

