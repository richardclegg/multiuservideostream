#!/usr/bin/env python
import sys, time
import fileinput
import math

n= 0
tots=[]
tots2= []
for line in fileinput.input():
    if line[0] == '#':
        continue
    parts= line.split()
    if len(tots) == 0:
        for p in parts:
            tots.append(float(p))
            tots2.append(float(p)*float(p))
    else:
        for (i,p) in enumerate(parts):
            tots[i]+= float(p)
            tots2[i]+= float(p)*float(p)
    n+= 1
for (t,t2) in zip(tots,tots2):
    mean= t/n
    meansq= t2/n
    sd= math.sqrt(meansq-(mean*mean))
    print mean, sd,
print
