#!/usr/bin/env python
import sys, time
import fileinput
import math

n= 0
tots=[]
for line in fileinput.input():
    if line[0] == '#':
        continue
    parts= line.split()
    if len(tots) == 0:
        for p in parts:
            tots.append(float(p))
    else:
        for (i,p) in enumerate(parts):
            tots[i]+= float(p)
    n+= 1
for t in tots:
    mean= t/n
    print mean,
print
