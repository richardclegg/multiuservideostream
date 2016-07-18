#!/usr/bin/env python
import getopt
import sys

import simulationModel
import streamOptions
import networkmodel.instanceCostNetwork as instanceCostNetwork
import networkmodel.simpleNetwork as simpleNetwork
import qoemodel.haversine as haversine

def printUsage():
    print >> sys.stderr, \
        'price_nearest.py [input_price.json] [input_locations.json] [n]', \
        '\nCompute a pricing system by locating the nearest n data centres\n', \
        'and weighting prices by distance'
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
    print >> sys.stderr, 'Need three arguments\n\n'
    printUsage()

input_price= args[0]
input_locations= args[1]
nlocs= 0
try:
	nlocs= int(args[2])
except:
	print >> sys.stderr, "Final argument must be integer"
	printUsage()

inprices= instanceCostNetwork.instanceCostNetwork()
inprices.parseInstCostFile(input_price,"")
inlocs= simpleNetwork.simpleNetwork()
inlocs.parseSimpleCostFile(input_locations,"")
hav=haversine.haversine()
for inloc in inlocs.nodes:
	combos=[]
	for inprice in inprices.nodes:
		d= hav.calcPairDelayNoCache(inloc.getLocation(),inprice.getLocation())	
		combos.append((d,inprice))
	s= sorted(combos, key=lambda x: x[0])
	inCost= 0.0
	outCost= 0.0
	instCost= 0.0
	weight= 0.0
	for i in range(nlocs):
		(d,dc)= s[i]
		if d == 0.0:
			inCost= dc.inCost
			outCost= dc.outCost
			instCost= dc.instCost
			weight= 1.0
			break
		inCost+= dc.inCost/d
		outCost+= dc.outCost/d
		instCost+= dc.instCost/d
		weight+= 1.0/d
		#print d,dc.getLat(),dc.getLong()
	print dc.getLat(),",", dc.getLong(),",", inCost/weight,",", outCost/weight,",", instCost/weight
