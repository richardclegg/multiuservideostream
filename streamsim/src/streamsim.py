#!/usr/bin/env python

import getopt
import sys

import simulationModel
import streamOptions


def printUsage():
    print >> sys.stderr, \
        'streamsim.py [options] [configfile.json]'
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
print >> sys.stderr, 'Initialising simulation'
sim= simulationModel.simulationModel(simOpts)
print >> sys.stderr, 'Simulating',simOpts.simDays,'days'
sim.simulate(simOpts.simDays)
print >> sys.stderr, 'Simulation finished'

