from hllrkfluxlimit2d import hllrkfluxlimit2d as hll
import cPickle
import numpy as np
import pylab as py

py.ion()

u = cPickle.load(file("helmholtz2d-fast.dat","r"))
#u = cPickle.load(file("shock2d-vertical.dat","r"))
uc = u.copy()

gamma = 1.4
hll.init(gamma, 0.1, 0.1, 0.2, 1.0)
pressure = lambda u : (gamma - 1) * (u[:,:,3] - 0.5 * u[:,:,1]**2 / u[:,:,0])

fig = py.figure(figsize=(12,12))
title = fig.suptitle("t = %0.2f"%hll.t)
py.subplot(221)
py.title("Density")
density = py.imshow(uc[:,:,0])
py.subplot(222)
py.title("velocity_x")
momx = py.imshow(uc[:,:,1]/uc[:,:,0])
py.subplot(223)
py.title("velocity_y")
momy = py.imshow(uc[:,:,2]/uc[:,:,0])
py.subplot(224)
py.title("Pressure_x")
energy = py.imshow(pressure(u))
py.draw()

i = 0
dt = 0.10
lastt = 0
while hll.t < 20:
  uc = hll.step(uc)
  print "[%0.2f] %f"%(hll.t,hll.dt)
  if (hll.t - lastt) >= dt:
    lastt += dt
    title.set_text("t = %0.2f"%hll.t)
    density.set_array(np.log(uc[:,:,0]+1))
    density.autoscale()
    momx.set_array(uc[:,:,1]/uc[:,:,0])
    momx.autoscale()
    momy.set_array(uc[:,:,2]/uc[:,:,0])
    momy.autoscale()
    energy.set_array(pressure(uc))
    energy.autoscale()
    py.draw()
    py.savefig("images-rkfluxlimit2D-helmholtz-fast/plot-%0.8d.png"%i)
  i += 1
