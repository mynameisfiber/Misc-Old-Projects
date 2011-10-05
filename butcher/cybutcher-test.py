#!/bin/env python

from cybutcher import butcher
import numpy as np
from time import time


a= np.array([[ 0. ,  0. ,  0. ],
             [ 0.5,  0.5,  0. ],
             [ 0. ,  0. ,  1. ]], dtype=np.float64)

f = lambda z,(w,v),dt,n : np.array([ v, -1./3. if z<dt else -2*v/z-w**n], dtype=np.float64)

dt = 0.1
numsteps = 50
t = np.arange(0,numsteps + 1,dtype=np.float64)*dt
data = [[1,0],]
n=1
runtime = 0
l1err = 0
for curt in t[:-1]:
  starttime = time()
  data.append( butcher(f,np.array(data[-1],np.float64),curt,dt,a, fargs=(dt,n)) )
  runtime += time() - starttime
  if curt != 0:
    l1err += np.abs(data[-1][0] - np.sin(curt)/curt)*dt

print "l1err = %f"%l1err
print "runtime = %f s"%(runtime / numsteps)
data = np.array(data)

#import pylab as py
#py.scatter(t, data[:,0])
#py.show()
