#!/usr/bin/env python

class locationProvider(object):
    
    def __init__(self, loc):
        self.loc= loc
        
    def getLocation(self):
        return self.loc
    
    def getRelativeTimeZone(self, units=24):
        return self.loc.getRelativeTimeZone(units)
    
    def getLat(self):
        return self.loc.lat
        
    def getLong(self):
        return self.loc.lon
        
    def getContinent(self):
        return self.loc.subcontinentalZone
        
    def getClosest(self, locations, qoeModel):
        maxDist= None
        bestLoc= None
        for l in locations:
            d= qoeModel.calcPairDelayNoCache(self.getLocation(),l.getLocation())
            if maxDist == None or d < maxDist:
                maxDist= d
                bestLoc= l
        return bestLoc
