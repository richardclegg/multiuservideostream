#!/usr/bin/env python

import routeModel


class hotPotatoRoute(routeModel.routeModel):
    """ A class to do hot potato routing"""

    def __init__(self):
        """ Initialise hotPotatoRoute"""
        self.routesSet= False

    def parseJSON(self,js,fName):
        """  parse JSON associated with this routeModel"""


    def getRoute(self, servers, start, end, qoeModel):
        """Return a route from start to end via servers
            given a particular QoE model -- route
            is not locations -- needs getLocation dereference"""
        best= servers[0]
        minDist= qoeModel.calcPairDelay(start.getLocation(),best.getLocation())
        minDist+= qoeModel.calcPairDelay(end.getLocation(),best.getLocation())
        for s in servers[1:]:
            dist= qoeModel.calcPairDelay(start.getLocation(),s.getLocation())
            dist+= qoeModel.calcPairDelay(end.getLocation(),s.getLocation())
            if dist < minDist:
                minDist=dist
                best= s
        return [start,best,end]
