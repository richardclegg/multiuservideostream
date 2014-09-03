#!/usr/bin/env python

import locationProvider


class demandLocation(locationProvider.locationProvider):
    """Class representing rate demand at a given location"""
    
    def __init__(self, loc, rate):
        locationProvider.locationProvider.__init__(self,loc)
        self.rate= float(rate)
 
    def __eq__(self, dl):
        
        if not (isinstance(dl, demandLocation)):
            return False
        if self.getLocation() == dl.getLocation() and self.rate == dl.rate:
            return True
        return False
        
    def __ne__(self, dl):
        return not self.__eq__(dl)
        
    def __lt__(self, dl):
        if not (isinstance(dl, demandLocation)):
            return False
        if self.rate < dl.rate:
            return True
        return False
        
    def __gt__(self, dl):
        if not (isinstance(dl, demandLocation)):
            return False
        if dl.rate > dl.rate:
            return True
        return False
