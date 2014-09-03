#!/usr/bin/env python

import math
import random
import sys

import demandModel
import location.demandLocation as demandLocation
import location.location as location
import location.user as user


class poisLogDemand(demandModel.demandModel):
    """ demand Model with poisson Arrivals and lognormal
    departures"""

    def __init__(self):
        """ Initialiser for Poisson/Lognormal model"""
        self.locDemand= []
        self.timeDemand= []
        self.timeInitialised= -1;
        self.initZone= None
        self.totDem= []

    def parseJSON(self,js,fName):
        """ parse the JSON in file fName which
        is generic to any demand model"""
        try:
            self.locFile= js.pop('locations')
            self.timeFile= js.pop('time_demand')
        except KeyError:
            print >> sys.stderr,'JSON file',fName, \
                'must contain locations, time_demand, '\
                'files'
            raise ValueError
        self.readLocationFile(self.locFile)
        self.readTimeFile(self.timeFile)

        try:
            seed= float(js.pop('randseed'))
            random.seed(seed)
        except KeyError:
            pass
        except ValueError as e:
            print >> sys.stderr,'randseed must be float in',fName
            raise e
        try:
            self.sigma=float(js.pop('session_sigma'))
        except ValueError:
            print >> sys.stderr,'JSON file',fName, \
                ' session_sigma must be a real number'
            raise ValueError
        except KeyError:
            print >> sys.stderr,'JSON file',fName, \
                ' session_sigma must be present'
            raise ValueError

        self.mu= None
        try:
            self.mu=float(js.pop("session_mu"))
        except ValueError:
            print >> sys.stderr,'JSON file',fName, \
                ' session_mu must be a real number'
            raise ValueError
        except KeyError:
            pass
        try:
            mean= float(js.pop("session_mean"))
            self.mu= math.log(mean)-self.sigma*self.sigma/2.0
        except ValueError:
            print >> sys.stderr,'JSON file',fName, \
                ' session_mean must be a real number'
            raise ValueError
        except KeyError:
            pass

        if self.mu == None:
            print >> sys.stderr,'JSON file',fName, \
                ' must specify either session_mean or session_mu ' \
                ' in poisLogDemand'
            raise ValueError



        self.base_arrival_rate= None
        try:
            self.base_arrival_rate= float(js.pop("arrival_rate"))
        except ValueError as e:
            print >> sys.stderr,'arrival_rate must be float in',fName
            raise e
        except KeyError:
            pass
        try:
            meanArrivals= float(js.pop("mean_daily_arrivals"))
            self.base_arrival_rate= self.arrivalsFromMean(meanArrivals)
        except ValueError as e:
            print >> sys.stderr, \
                'mean_daily_arrivals must be float in',fName
            raise e
        except KeyError:
            pass
        if self.base_arrival_rate == None:
            print >> sys.stderr, 'Must specify either arrival_rate', \
                'or mean_daily_arrivals in poisLogDemand',fName

    def arrivalsFromMean(self, meanArrivals):
        """ Return base arrival rate given mean daily arrivals"""
        totDaily= 0.0
        for i in range (len(self.timeDemand)-1,-1,-1):
            self.doTimeZoneInit(i)
            totDaily+= self.totDemand
        return meanArrivals*len(self.timeDemand)/(totDaily*60*60*24)

    def readLocationFile(self, fileName):
        """Read a file with csv location triples"""
        self.locDemand= location.location.readLocationFile(fileName,demandLocation.demandLocation)
        if len(self.locDemand) == 0:
            print >> sys.stderr, 'Location file should contain at least one location',fileName
            raise ValueError("Must have at least one location in location file")



    def readTimeFile(self, fileName):
        """Read a file with time rate multipliers"""
        try:
            f=open(fileName)
        except IOError as e:
            print >> sys.stderr,'Cannot open time file',fileName
            raise ValueError ('Cannot open time file %s ',fileName)
        while True:
            l= f.readline()
            if l == '':
                break
            locs= location.location.removeCommentsAndSplit(l)
            if locs == None:
                continue
            # Ignore comments and blank lines
            try:
                td= float(locs[0])
                self.timeDemand.append(td)
                #print "READ TIME",td, len(self.timeDemand)
            except ValueError as e:
                print >> sys.stderr, 'Time file should contain only floats',fileName
                raise e
        f.close()
        if len(self.timeDemand) == 0:
            print >> sys.stderr, 'Time file should contain at least one float',fileName
            raise ValueError("Must have at least one time in demand file")

    def doTimeZoneInit(self, timeAdjust):
        """Initialise departure rates to stop repeated calculations
        This gives departure rates from locations in the same time
        zone"""
        self.totDemand= 0.0
        self.locCumDemand= []
        noZones=len(self.timeDemand)
        for l in self.locDemand:
            lzone= (timeAdjust+l.getRelativeTimeZone(noZones))%noZones
            #print "local zone",lzone
            self.totDemand+= l.rate*self.timeDemand[lzone]
            self.locCumDemand.append(self.totDemand)
        self.initZone= timeAdjust
        #print [float(l.rate)/self.totDemand for l in self.locDemand]
        #print self.locCumDemand


    def chooseLocation(self):
        """Pick location"""
        r= random.random()*self.totDemand
        for (i,c) in enumerate(self.locCumDemand):
            if c > r:
                return i
        return len(self.locDemand)-1

    def whichTime(self,time):
        sinceMidnight= time%(24*60*60)
        proportion= float(sinceMidnight)/(24*60*60)
        zone= int(math.floor(proportion*len(self.timeDemand)))
        return zone


    def nextArrival(self,time):
        """Create a user object for the next user to arrive"""
        zone= self.whichTime(time)
        #print "Time zone",zone,"time",time,"since midnight", \
        #    float(time%(24*60*60))/(24*60*60)
        if zone != self.initZone:
            self.doTimeZoneInit(zone)

        loc= self.locDemand[self.chooseLocation()].getLocation()
        arrivalRate=self.totDemand*self.base_arrival_rate
        delta= random.expovariate(arrivalRate)
        life= random.lognormvariate(self.mu,self.sigma)
        #print "rate",arrivalRate,"delta",delta,"life",life

        thisuser= user.user(loc,time+delta,time+delta+life)
        return thisuser


