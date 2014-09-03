#!/usr/bin/env python

import routeModel


class stayOnRoute(routeModel.routeModel):
    """ A class to route traffic for longest part of journey
        on managed network"""

    def __init__(self):
        """ Initialise stayOnRoute"""


    def parseJSON(self,js,fName):
        """  parse JSON associated with this routeModel"""


    def getRoute(self, servers, start, end, qoeModel):
        """Return a route from start to end (both users) via servers
            given a particular QoE model"""
        startServ= servers[0]
        endServ= servers[0]
        startDist= qoeModel.calcPairDelay(start.getLocation(),startServ.getLocation())
        endDist= qoeModel.calcPairDelay(end.getLocation(),endServ.getLocation())
        for s in servers[1:]:
            sd= qoeModel.calcPairDelay(start.getLocation(),s.getLocation())
            if sd < startDist:
                startDist= sd
                startServ= s
            ed= qoeModel.calcPairDelay(end.getLocation(),s.getLocation())
            if ed < endDist:
                endDist= ed
                endServ= s
        if startServ == endServ:
            return [start,startServ,end]
        return [start,startServ,endServ,end]
