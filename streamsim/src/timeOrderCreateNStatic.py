#!/usr/bin/env python

#!/usr/bin/env python

import getopt
import sys

import streamOptions
import location.cluster as cluster
import location.demandLocation as demandLocation
import servermodel.nDynamic as nDynamic


def printUsage():
    print >> sys.stderr, \
        'createNStatic.py [options] [configfile.json] [max no servers] [max_locs]'
    print >> sys.stderr, \
        '\t\t-h -- print this help and exit'
    sys.exit()

try:
    (opts, args) = getopt.getopt(sys.argv[1:], 'h')
except getopt.GetoptError, err:
    print >> sys.stderr, 'Unrecognised option', err
    printUsage()

for (o,a) in opts:
    if o == '-h':
        printUsage()
if len(args) != 3:
    print >> sys.stderr, 'Must be three args'
    printUsage()
fileName=args[0]
maxServ=int(args[1])
noLocs= int(args[2])
print >> sys.stderr, 'Reading configuration from',fileName
simOpts= streamOptions.streamOptions()
if not simOpts.readJson(fileName):
    sys.exit()
baselocs= simOpts.demMod.locDemand
choice= simOpts.netMod.locations()  
timeSteps= len(simOpts.demMod.timeDemand)
width= 60*60*24/timeSteps
time=int(width/2)
# Start in middle of first time step
for t in range(timeSteps):   
    locs=[]
    for l in baselocs:
        lzone= (time+l.getRelativeTimeZone(timeSteps))%timeSteps
        tmult=simOpts.demMod.timeDemand[lzone]
        nl= demandLocation.demandLocation(l.getLocation(),l.rate*tmult)
        locs.append(nl)
        
    locs.sort()
    locs.reverse()
    maxLocs=locs[0:noLocs]
    for l in maxLocs:
        lzone= (time+l.getRelativeTimeZone(timeSteps))%timeSteps
        tmult=simOpts.demMod.timeDemand[lzone]
        #print time,l.getLocation().lat,l.getLocation().lon,lzone,l.rate
    for i in range(maxServ):
        nServ= i+1
        clusters= cluster.cluster.clusterDemandLocs(maxLocs, \
            nServ, simOpts.qoeMod)
        centres= nDynamic.nDynamic.chooseServers(clusters,choice,simOpts.qoeMod)
        sys.stdout.write(str(t)+",")
        for (i,c) in enumerate(centres):
            if i > 0:
                sys.stdout.write(",")
            sys.stdout.write(str(c.getLocation().lat)+","+str(c.getLocation().lon))
        print
    time+= width
    print time
