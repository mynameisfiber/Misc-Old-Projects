#!/usr/bin/python

from __future__ import division
from numpy import random, pi
import threading
from time import sleep
from sys import stdout

####CONFIG#####
threads = 8
pointsperthread = 1e6
timeout = 5 #seconds
###############

class PiThread(threading.Thread):
  def __init__(self, maxpoints):
    threading.Thread.__init__(self)
    self.maxpoints = maxpoints
    self.points = 0
    self.interiorpoints = 0
    self.status = 0.0

  def run(self):
    notify = 0.25 * self.maxpoints
    print "%s: Starting" % self.name
    random.seed(None)
    while self.points < self.maxpoints:
      self.status = self.points * 100 / self.maxpoints
      x,y = random.rand(2)
      self.interiorpoints += int( x**2 + y**2 <= 1 )
      self.points += 1
    print "%s: Done" % self.name

nodes = []
#Initialize threads and start them
for node in range(threads):
  nodes.append( PiThread(pointsperthread) )
  nodes[-1].start()

#Retrieve status from active nodes and output (cure for my impatience).
#This will continue as long as any thread is still working (except this thread)
#while threading.active_count() > 1:
#  print ("%.2f%% "*threads) % tuple([node.status for node in nodes]) + "\r",
#  stdout.flush()
#  sleep( timeout )

for node in nodes:
  node.join()

#Retrieve solutions from each node
totalpoints = 0
totalinteriorpoints = 0
for node in nodes:
  print "Node %s found pi = %f (i=%d,t=%d)"%(node.name, 4.0*node.interiorpoints/node.points,node.interiorpoints,node.points)
  totalpoints += node.points
  totalinteriorpoints += node.interiorpoints
calcpi = 4.0 * totalinteriorpoints / totalpoints

print "\n"+"="*25
print "Points used:       %d" % totalpoints
print "Interior Points:   %d" % totalinteriorpoints
print "Calculated Pi:     %0.32f" % calcpi
print "Compared to numpy: %0.32f" % abs(calcpi - pi)
