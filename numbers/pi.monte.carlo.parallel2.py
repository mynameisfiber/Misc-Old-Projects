#!/usr/bin/python

from __future__ import division
from numpy import random, pi
from multiprocessing import Process, Queue
from time import sleep, time

####CONFIG#####
threads = 32
pointsperthread = 1e5
###############

def run(name,maxpoints,q):
  #print "Node %d: Starting"%name
  starttime = time()
  notify = 0.25 * maxpoints
  random.seed(None)
  points = 0
  interiorpoints = 0
  while points < maxpoints:
    x,y = random.uniform(0,1,2)
    interiorpoints += int( x**2 + y**2 <= 1 )
    points += 1
  endtime = time()
  q.put((name,interiorpoints,points,endtime-starttime))
  #print "Node %d: Done"%name

#Initialize threads and start them
p = []
q = Queue(threads)
for name in range(threads):
  p.append(Process(target=run, args=(name,pointsperthread,q)))
  p[-1].start()

#Retrieve solutions from each node
totalpoints = 0
totalinteriorpoints = 0
totaltime = 0
for i in range(threads):
  name, interiorpoints, points, extime = q.get(block=True)
  print "Node %d: \t Found pi = %f (i=%d,t=%d)"%(name,4.0*interiorpoints/points,interiorpoints,points)
  totalpoints += points
  totalinteriorpoints += interiorpoints
  totaltime += extime
averagetime = totaltime / threads
calcpi = 4.0 * totalinteriorpoints / totalpoints

print "\n"+"="*25
print "Points used:       %d" % totalpoints
print "Interior Points:   %d" % totalinteriorpoints
print "Calculated Pi:     %0.32f" % calcpi
print "Compared to numpy: %0.32f" % abs(calcpi - pi)
print "Time per thread:   %0.8f" % averagetime
print "Total CPU time:    %0.8f" % totaltime
