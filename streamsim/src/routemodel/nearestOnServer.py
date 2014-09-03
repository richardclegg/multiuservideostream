#!/usr/bin/env python

import routeModel


class nearestOnServer(routeModel.routeModel):
    """ A class to route to the nearest possible server """

    def __init__(self):
        """ Initialise nearestOnRoute"""
        self.routesSet= False

    def parseJSON(self,js,fName):
        """  parse JSON associated with this routeModel"""


    def getRoute(self, servers, start, end, qoeModel):
        """Return a route from start to end via servers
            given a particular QoE model -- route
            is not locations -- needs getLocation dereference"""
        best= servers[0]
        minDist= qoeModel.calcPairDelay(start.getLocation(),best.getLocation())
        for s in servers[1:]:
            dist= qoeModel.calcPairDelay(start.getLocation(),s.getLocation())
            if dist < minDist:
                minDist=dist
                best= s
        return [start,best,end]

    def symmetric(self):
        """This route model is not symmetric"""
        return False
