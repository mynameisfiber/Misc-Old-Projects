from hllrkfluxlimit2d import hllrkfluxlimit2d as hll
import cPickle
import numpy as np
import pylab as py

#py.ion()

#u = cPickle.load(file("data/helmholtz2d-subsonic.dat","r"))
#uc = cPickle.load(file("data/shock2d-diagonal.dat","r"))

def energy(gamma, pressure, u):
  return pressure / (gamma - 1) + 0.5 * (u[1]*u[1]+u[2]*u[2]) / u[0]

def shock2ddiagonal(u):
  for x in range(u.shape[0]):
    for y in range(u.shape[1]):
      if x < y:
        u[x,y,0] = 1.0
        u[x,y,3] = energy(1.4,1., u[x,y,:])
      else:
        u[x,y,0] = .1
        u[x,y,3] = energy(1.4,0.125, u[x,y,:])
  return u

#def helmholtz(u):                                                                         
#  a = np.array([ 2. ,  1.  ,  0. , 6.5])
#  a[3] = energy(1.4, 2.5, a)
#  b = np.array([ 1. , -0.5 ,  0.  ,  6.375])
#  b[3] = energy(1.4, 2.5, b)
#  xintmin = 0.25 * u.shape[0]
#  xintmax = 0.75 * u.shape[0]
#  for x in range(u.shape[0]):
#    for y in range(u.shape[1]):
#      if xintmin < x < xintmax:
#        u[x,y,:] = a.copy()
#      elif xintmin > x or xintmax < x:
#        u[x,y,:] = b.copy()
#      else:
#        u[x,y,:] = a.copy()
#        u[x,y,2] = 0.01*u[x,y,1]*np.sin(2*np.pi*y/(u.shape[0]-1))
#        #u[x,y,1] = 0.0
#        u[x,y,3] = energy(1.4, 2.5, u[x,y,:])
#  return u

def helmholtz1(u):
  gamma = 1.4
  P = 2.5
  amp = 1e-2
  drat = 2.0
  vflow = 0.5
  xmin = 0.25 * u.shape[0]
  xmax = 0.75 * u.shape[0]
  for x in range(u.shape[0]):
    for y in range(u.shape[1]):
      u[x,y,:] = np.array([1.0, vflow+amp*(np.random.random() - 0.5), amp*(np.random.random() - 0.5), 0])
      if xmin < x < xmax:
        u[x,y,0] = drat
        u[x,y,1] = -drat*(vflow + amp * (np.random.random()-0.5))
        u[x,y,2] = drat * amp * (np.random.random() - 0.5)
      u[x,y,3] = energy(gamma, P, u[x,y,:])
  return u

def helmholtz2(u):
  gamma = 1.4
  P = 2.5
  amp = 1e-2
  drat = 2.0
  vflow = 0.5
  xmin = 0.25 * u.shape[0]
  xmax = 0.75 * u.shape[0]
  for x in range(u.shape[0]):
    for y in range(u.shape[1]):
      u[x,y,:] = np.array([1.0, vflow, amp*np.sin(np.pi*x/(u.shape[0]-1)), 0])
      if xmin < x < xmax:
        u[x,y,0] = drat
        u[x,y,1] = -drat*(vflow)
        u[x,y,2] = drat * amp * np.sin(np.pi*x/(u.shape[0]-1))
      u[x,y,3] = energy(gamma, P, u[x,y,:])
  return u

#uc = helmholtz2(np.zeros((1024,1024,4),dtype=np.float64))
uc = shock2ddiagonal(np.zeros((1024,1024,4)))

gamma = 1.4
hll.init(gamma, 2./uc.shape[0], 2./uc.shape[1], 0.8, 1.9)
pressure = lambda u : (gamma - 1) * (u[:,:,3] - 0.5 * (u[:,:,1]**2 + u[:,:,2]**2)/ u[:,:,0])

fig = py.figure(figsize=(12,12))
title = fig.suptitle("t = %0.2f"%hll.t)
py.subplot(221)
py.title("Density")
density = py.imshow(uc[:,:,0])
py.colorbar()
py.subplot(222)
py.title("velocity_x")
momx = py.imshow(uc[:,:,1]/uc[:,:,0])
py.colorbar()
py.subplot(223)
py.title("velocity_y")
momy = py.imshow(uc[:,:,2]/uc[:,:,0])
py.colorbar()
py.subplot(224)
py.title("Pressure")
energy = py.imshow(pressure(uc))
py.colorbar()
py.draw()

i = 0
dt = 0.05
lastt = 0
while True: #hll.t < 20:
  uc = hll.step(uc)
  print "[%0.2f] %f"%(hll.t,hll.dt)
  if (hll.t - lastt) >= dt or i == 0:
    if i != 0:
      lastt += dt
    title.set_text("t = %0.2f"%hll.t)
    density.set_array(uc[:,:,0])
    density.autoscale()
    momx.set_array(uc[:,:,1]/uc[:,:,0])
    momx.autoscale()
    momy.set_array(uc[:,:,2]/uc[:,:,0])
    momy.autoscale()
    energy.set_array(pressure(uc))
    energy.autoscale()
    py.draw()
    py.savefig("tmp/plot-%0.8d.png"%i)
  i += 1
