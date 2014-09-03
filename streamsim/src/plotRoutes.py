#!/usr/bin/env python

#!/usr/bin/env python

import getopt
import sys

import simulationModel
import streamOptions
import servermodel.nDynamic
import location.cluster as cluster
import sessionmodel.session as session


def printUsage():
    print >> sys.stderr, \
        'plotRoutes.py [options] [configfile.json]'
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
if len(args) > 1:
    print >> sys.stderr, 'Too many arguments'
    printUsage()
if len(args) == 1:
    fileName=args[0]
else:
    fileName='config.json'
print >> sys.stderr, 'Reading configuration from',fileName
simOpts= streamOptions.streamOptions()
if not simOpts.readJson(fileName):
    sys.exit()

nUsers= 12
noServers= simOpts.serverMod.noServers
users=[]
sess=session.session(0)
for i in range(nUsers):
    user= simOpts.demMod.nextArrival(60*60*i)
    users.append(user)
    sess.addUser(user)
time=0
clusters= cluster.cluster.clusterUsers(users,noServers, simOpts.qoeMod)
simOpts.serverMod.updateServers(time,sess,simOpts.netMod,simOpts.qoeMod, \
                    simOpts.routeMod, simOpts.demMod)
qoe= simOpts.qoeMod.calcSessionDelay(sess,simOpts.routeMod)
costs= simOpts.netMod.getCostTuple(sess,60,simOpts.routeMod)
inout={}
between={}
fullbw= simOpts.netMod.fullStream
partbw= simOpts.netMod.fullStream/nUsers+simOpts.netMod.compressedStream* \
                (nUsers-1)/nUsers
rdict={}
indict={}
outdict={}
for r in sess.routes:
    #for i in r:
    #    print >> sys.stderr, i.getLocation().lat,i.getLocation().lon,
    #print >> sys.stderr
    if not indict.has_key(r[0]):
        indict[r[0]]= True
        h1= r[0].getLocation()
        h2= r[1].getLocation()
        if not inout.has_key((h1,h2)):
            inout[(h1,h2)]= fullbw+partbw
        else:
            inout[(h1,h2)]+= fullbw+partbw
    if not indict.has_key(r[-1]):
        indict[r[-1]]= True
        h1= r[-1].getLocation()
        h2= r[-2].getLocation()
        if not inout.has_key((h1,h2)):
            inout[(h1,h2)]= partbw+fullbw
        else:
            inout[(h1,h2)]+= partbw+fullbw
    for i in range(1,len(r)-2):
        if rdict.has_key((r[i],r[i+1],r[0])):
            continue
        rdict[r[i],r[i+1],r[0]]= True
        if r[i].getLocation() < r[i+1].getLocation():
            h1= r[i].getLocation()
            h2= r[i+1].getLocation()
        else:
            h1= r[i+1].getLocation()
            h2= r[i].getLocation()
        if not between.has_key((h1,h2)):
            between[(h1,h2)]= partbw
        else:
            between[(h1,h2)]+= partbw
for (link,val) in inout.items():
    print link[0].getLocation().lat,link[0].getLocation().lon, \
        link[1].getLocation().lat,link[1].getLocation().lon, val,1
for (link,val) in between.items():
    print link[0].getLocation().lat,link[0].getLocation().lon, \
        link[1].getLocation().lat,link[1].getLocation().lon, val,2
               

