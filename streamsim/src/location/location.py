#!/usr/bin/env python

import sys, math


class location (object):
    """ Class representing a location on the surface of the earth --
    latitude, longtitude and (optional) subcontinentalZone code"""

    def __init__(self, lat, lon, contcode=None):
        """Initialise with lat, long and optional subcontinental zone code"""
        self.lat= float(lat)
        self.lon= float(lon)
        self.radlat= float(lat)*math.pi/180
        self.radlon= float(lon)*math.pi/180
        self.subcontinentalZone= str(contcode)

    def __eq__(self,loc):
        """ Over ride equality to ignore continental zone in case one loc has it
        defined another not"""
        if not (isinstance(loc,location)):
            return False
        if self.lat != loc.lat:
            return False
        if self.lon != loc.lon:
            return False
        return True

    def __ne__ (self,loc):
        return not self.__eq__(loc)

    def getRelativeTimeZone(self, units=24):
        """Divide longitude into a number of equal size units centred on
        zero and return which unit this is in with 0 being the Grenwich meridian.
        For simplicity the units are numbered 0 to units-1 rather than negatively"""

        return int(round(((self.lon/360)%1)*units))

    def getLocation(self):
        return self

    def getLat(self):
        return self.lat

    def getLong(self):
        return self.lon

    def getContinent(self):
        return self.subcontinentalZone
    
    def convertToCartesian(self):
        x= math.cos(self.radlat)*math.cos(self.radlon)
        y= math.cos(self.radlat)*math.sin(self.radlon)
        z= math.sin(self.radlat)
        return(x,y,z)
        
        
    @staticmethod
    def convertFromCartesian((x,y,z)):
        ''' create a location from cartesian '''
        R= math.sqrt(x*x+y*y+z*z)
        if R == 0:
            return location(0,0)
        lat = math.asin(z / R)*180/math.pi
        lon = math.atan2(y, x)*180/math.pi
        return location(lat,lon)
    
    @staticmethod
    def mergeLocations(loclist):
        ''' Create a location which is the average of a list of 
            locations'''
        totals= [0.0,0.0,0.0]
        for l in loclist:
            totals= map(sum,zip(totals,l.convertToCartesian()))
        return location.convertFromCartesian(totals)

    @staticmethod
    def weightedMergeLocations(loclist, weights):
        ''' Create a location which is the average of a list of 
            locations'''
        totals= [0.0,0.0,0.0]
        for (l,w) in zip(loclist,weights):
            g= lambda x: x*w
            tmp= map(g,l.convertToCartesian())
            totals= map(sum,zip(totals,tmp))
        return location.convertFromCartesian(totals)        
        
    @staticmethod
    def mergeTwoLocations(loc1, loc2, weight1, weight2):
        (x1,y1,z1)= loc1.convertToCartesian()
        (x2,y2,z2)= loc2.convertToCartesian()
        total= weight1+weight2
        weight1/= total
        weight2/= total
        x3= x1*weight1+x2*weight2
        y3= y1*weight1+y2*weight2
        z3= z1*weight1+z2*weight2
        return location.convertFromCartesian((x3,y3,z3))
        

    @staticmethod
    def removeCommentsAndSplit(line):
        (line,_,_)= line.partition('%')
        (line,_,_)= line.partition('#')
        if line == '\n' or line == '\r' or line == '':
            return None
        locs=line.split(',')
        return locs

    @staticmethod
    def readLocationFile(fileName,initialiser):
        """Static function reads a location name and returns
        a list of locations or prints an error and raises ValueError"""

        loclist=[]
        try:
            f=open(fileName)
        except IOError as e:
            print >> sys.stderr,'Cannot open location file',fileName,e
            raise ValueError ('Cannot open location file %s ',fileName)
        while True:
            l= f.readline()
            if l == '':
                break
            locs= location.removeCommentsAndSplit(l)
            if locs == None:
                continue
            # Ignore comments and blank lines

            if len(locs) < 3 or len(locs) > 4:
                print >> sys.stderr, 'In location file',fileName, \
                    'lines must be 3 or 4 tuple',locs
                raise ValueError
            try:
                l0= float(locs[0])
                l1= float(locs[1])
                l2= float(locs[2])
            except:
                print >> sys.stderr, 'In location file',fileName, \
                    'lines must begin with 3 tuple of floats',l
                raise ValueError

            if len(locs) == 3:
                loc= location(l0,l1)
            else:
                loc= location(l0,l1,locs[3].strip())
            demloc= initialiser(loc,l2)
            loclist.append(demloc)
        f.close()
        return loclist
