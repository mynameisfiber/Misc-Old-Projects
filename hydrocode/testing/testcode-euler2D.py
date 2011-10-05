from hlleuler2d import hlleuler2d as hll
import cPickle
import numpy as np
import pylab as py

u = cPickle.load(file("shock2d-vertical.dat","r"))
uc = u.copy()

gamma = 1.4
hll.init(gamma, 0.1, 0.1, 0.2)

for i in range(500):
  uc = hll.step(uc)
  py.clf()
  py.subplot(221)
  py.title("i=%0.2f"%hll.t)
  py.ylabel("Density")
  py.imshow(uc[:,:,0])
  py.subplot(222)
  py.ylabel("Momentum_x")
  py.imshow(uc[:,:,1])
  py.subplot(223)
  py.ylabel("Momentum_y")
  py.imshow(uc[:,:,2])
  py.subplot(224)
  py.ylabel("Energy")
  py.imshow(uc[:,:,3])
  py.savefig("images-euler2D/plot-%0.8d.png"%i)
