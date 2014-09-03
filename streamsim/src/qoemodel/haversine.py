#!/usr/bin/env python

import math

import qoeModel


class haversine(qoeModel.qoeModel):
    """A class which represents user qoe for traffic on a route
    using haversine distance"""

    earthradius= 6.371e6

    def __init__(self):
        """Empty initialiser"""
        self.slope=0.018
        self.intercept= 20
        super(haversine,self).__init__()

    @staticmethod
    def haversin(angle):
        """Calculate the haversin for an angle"""
        return ((1.0 - math.cos(angle*math.pi/180.0))/2.0)

    @staticmethod
    def haversinrad(angle):
        """Calculate the haversin for an angle"""
        return ((1.0 - math.cos(angle))/2.0)
    @staticmethod
    def haverdist(loc1, loc2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """


        # haversine formula
        dlon = loc2.radlon - loc1.radlon
        dlat = loc2.radlat - loc1.radlat
        aux = haversine.haversinrad(dlat) + math.cos(loc1.radlat) * math.cos(loc2.radlat) * haversine.haversinrad(dlon)
        # print  loc1.lon,loc1.lat,"  ",loc2.lon,loc2.lat,"aux =",aux
        dist = 2 * haversine.earthradius * math.asin(math.sqrt(aux));
        return dist

    def calcPairDelayNoCache(self,loc1,loc2):
        dist= self.slope * haversine.haverdist(loc1,loc2) + self.intercept
        return dist

    def calcPairDelay(self,loc1,loc2):
        """Calculate distance between pair of locations"""
        dist= super(haversine,self).fromCache(loc1,loc2)
        if dist != None:
            return dist
        dist= self.slope * haversine.haverdist(loc1,loc2) + self.intercept
        super(haversine,self).toCache(loc1,loc2,dist)
        return dist


