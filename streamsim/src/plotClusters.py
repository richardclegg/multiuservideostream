#!/usr/bin/env python

#!/usr/bin/env python

import getopt
import sys

import simulationModel
import streamOptions
import servermodel.nDynamic
import location.cluster as cluster


def printUsage():
    print >> sys.stderr, \
        'plotClusters.py [options] [configfile.json]'
    print >> sys.stderr, \
        '\t\t-h -- print this help and exit'
    print >> sys.stderr, \
        'Simulation by default reads a file config.json'
    sys.exit()

try:
    (opts, args) = getopt.getopt(sys.argv[1:], 'h')
except getopt.GetoptError, err:
    print >> sys.stderr, 'Unrecognised option', err
    printUsage()

for (o,a) in opts:
    if o == '-h':
        printUsage()
if len(args) > 2:
    print >> sys.stderr, 'Too many arguments'
    printUsage()
nUsers= 100
if len(args) == 2:
    fileName = args[0]
    nusers= int(args[1])
elif len(args) == 1:
    fileName=args[0]
else:
    fileName='config.json'
print >> sys.stderr, 'Reading configuration from',fileName
simOpts= streamOptions.streamOptions()
if not simOpts.readJson(fileName):
    sys.exit()


noServers= simOpts.serverMod.noServers
users=[]
for i in range(nUsers):
    user= simOpts.demMod.nextArrival(60*60*i)
    users.append(user)

clusters= cluster.cluster.clusterUsers(users,noServers, simOpts.qoeMod)
choice= simOpts.netMod.locations() 
servers= servermodel.nDynamic.nDynamic.chooseServers(clusters, choice, simOpts.qoeMod)
for (i,c) in enumerate(clusters):
    for u in c.users:
        print u.getLocation().lat,u.getLocation().lon,i,1
    print c.getLocation().lat,c.getLocation().lon,i,2
    print servers[i].getLocation().lat, servers[i].getLocation().lon,i,3

