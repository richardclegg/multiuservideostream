#!/usr/bin/env python

import locationProvider


class datacentre(locationProvider.locationProvider):
    """Class representing a data center at a given location"""

    def __init__(self, loc, inCost,outCost,instcost=0):
        locationProvider.locationProvider.__init__(self,loc)
        self.inCost= inCost
        self.outCost= outCost
        self.instCost=instcost
