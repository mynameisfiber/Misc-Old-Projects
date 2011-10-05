from hllrkfluxlimit import hllrkfluxlimit as hll
import cPickle
import numpy as np
import pylab as py

u = cPickle.load(file("1dshock.dat","r"))

gamma = 1.4
hll.init(gamma, 0.01, 0.8,1.5)

#for i in range(5000):
#  uc = hll.step(uc)
#  if i%10 == 0:
#    py.clf()
#    py.title("i=%d"%i)
#    py.plot(uc[:,0],label="density")
#    py.plot(uc[:,1]/uc[:,0],label="velocity")
#    py.plot(uc[:,2],label="energy")
#    py.legend()
#    py.savefig("images-rkfluxlimit/plot-%0.8d.png"%i)

py.ion()
density,  = py.plot(u[:,0],label="density")
velocity, = py.plot(u[:,1]/u[:,0],label="velocity")
energy,   = py.plot(u[:,2],label="energy")
py.legend()

i = 0
while True:
  u = hll.step(u)
  if i%10 == 0:
    py.title("i=%d"%i)
    density.set_ydata(u[:,0].copy())
    velocity.set_ydata(u[:,1]/u[:,0])
    energy.set_ydata(u[:,2].copy())
    py.draw()
  i += 1
