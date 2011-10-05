from hlleuler import hlleuler as hll
import cPickle
import numpy as np
import pylab as py

u = cPickle.load(file("1dshock.dat","r"))
uc = u.copy()

gamma = 1.4
hll.init(gamma, 0.1, 0.8)

for i in range(100):
  uc = hll.step(uc)
  py.clf()
  py.title("i=%d"%i)
  py.plot(uc[:,0],label="density")
  py.plot(uc[:,1]/uc[:,0],label="velocity")
  py.plot(uc[:,2],label="energy")
  py.legend()
  py.savefig("images-euler/plot-%0.8d.png"%i)
