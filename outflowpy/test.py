#!/usr/bin/python

import numpy, cPickle, sys
from tvd import tvd
from outflows import inject

maxstep = -1
if len(sys.argv) == 2:
  maxstep = int(sys.argv[1])

n = 50
u = numpy.zeros((4,n,n,n))
#u = numpy.random.random((4,n,n,n))*5
u[0,:,:,:] = 1

nstep = 0
while True:
  if nstep == maxstep:
    break
  u = inject(u, [int(x) for x in numpy.random.random(3)*n], 100)
  u,dt,maxv = tvd.step(u,0.65)
  print "nstep = %d, dt = %f, maxv = %f"%(nstep,dt,maxv)
  if nstep % 10 == 0:
    cPickle.dump(u[:,:,n/2,0],file("data/output-%08d"%nstep,"w+"))
  nstep += 1
