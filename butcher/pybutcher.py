#!/bin/env python
#
# pybutcher: implement cybutcher in order to solve the questions posed in the first
#            assignment of computational physics
# author:    micha gorelick, gorelick@nyu.edu
# date:      30/09/10
#

from __future__ import division
import cybutcher as cyb
import numpy as np

def tableau(kind):
  if kind == "euler":
    return np.array([[ 0 , 0 ],   
                     [ 0 , 1 ]], dtype=cyb.DTYPE)
  elif kind == "midpoint":
    return np.array([[ 0. ,  0. ,  0. ],
                     [ 0.5,  0.5,  0. ],
                     [ 0. ,  0. ,  1. ]], dtype=cyb.DTYPE)
  elif kind == "rk4":
    return np.array([[ 0.  , 0.   , 0.   , 0.   , 0.    ],
                     [ 0.5 , 0.5  , 0.   , 0.   , 0.    ],
                     [ 0.5 , 0.   , 0.5  , 0.   , 0.    ],
                     [ 1.  , 0.   , 0.   , 1.   , 0.    ],
                     [ 0.  , 1./6., 1./3., 1./3., 1./6. ]], dtype=cyb.DTYPE)
  elif kind == "rk5":
    return np.array([[0,0,0,0,0,0,0],
                     [1./4., 1./4.,0,0,0,0,0],
                     [3./8.,3./32.,9./32.,0,0,0,0],
                     [12./13.,1932./2197., -7200./2197., 7296./2197.,0,0,0],
                     [1.,439./216.,-8.,3680./513., -845./4104.,0,0],
                     [1./2., -8./27., 2., -3544./2565., 1859./4104., -11./40.,0],
                     [0, 16./135., 0., 6656./12825., 28561./56430., -9./50., 2./55.]], dtype=cyb.DTYPE)


def calc_polytrope_butcher(n, method="rk4", zmin=0, zmax=10, imax=10, analytic=None):
  f = lambda z, (w,v), dt, n : np.array([v, -2*v/z - np.power(w,n) if z>dt else -1./3.], dtype=cyb.DTYPE)
  dz = (zmax - zmin)/(imax - 1)
  data = np.zeros((imax, 3), dtype=cyb.DTYPE)
  data[0,0:3] = [zmin, 1.0, 0.0]
  l1error = 0.0
  for i in range(1,imax):
    z = zmin + (i-1)*dz
    data[i,0] = zmin + i*dz
    data[i,1:3],k = cyb.butcher(f, data[i-1,1:3], z, dz, tableau(method),fargs=(dz,n))
    if analytic and z>0:
      l1error += np.fabs(data[i,1]-analytic(data[i,0]))
  return data, l1error*dz


def find_root(x1,x2):
  """Return the root of a linear function with two points, x1 and x2, fixed."""
  return x1[0]-x1[1]*(x2[0]-x1[0])/(x2[1]-x1[1])


def find_radius(data):
  """Finds the first root of the given data.  First an approximate solution is
     found which is then refined by using a linear approximation.
     Data is in the form:
       data = [ [x1, y1], ..., [xN, yN]]"""
  for i in range(data.shape[0]):
    if data[i,1] < 0:
      return find_root(data[i-1,:3],data[i,:3])
    elif np.isnan(data[i,1]):
      return data[i-1,0]
  return -1

def color_cycle():
  c = "bgrcmk"
  i = 0
  while True:
    yield c[i]
    i = (i+1)%len(c)


def linestyle_cycle():
  l = ['-','--','-.',':']
  i = 0
  while True:
    yield l[i]
    i = (i+1)%len(l)


def marker_cycle():
  m = "so^>v<dph+x1234HD|_"
  i = 0
  while True:
    yield m[i]
    i = (i+1)%len(m)


if __name__ == "__main__":
  import pylab as py

  cc = color_cycle()
  cm = marker_cycle()
  cl = linestyle_cycle()

  py.figure(1)
  l1errors = {"euler":[], "midpoint":[], "rk4":[], "rk5":[]}
  n1_analytical = lambda z : np.sin(z)/z
  for method in l1errors.keys():
    data, l1 = calc_polytrope_butcher(1, method=method, analytic=n1_analytical)
    l1errors[method].append([10./9.,l1])
    py.plot(data[:,0],data[:,1],label="%s with L1=%0.2f"%(method, l1),c=cc.next(),marker=cm.next(),linestyle=cl.next())
  py.plot(data[:,0],n1_analytical(data[:,0]),label="Analytic Solution",c=cc.next(),marker=cm.next(),linestyle=cl.next(),linewidth=4)
  py.legend(loc="upper left")
  py.xlabel("z")
  py.axhline(y=0,color=(.8,)*3)
  py.ylabel("w(z)")
  py.title("n=1 polytrope solved numerically with dz=1.0 using various methods")
  py.xlim((-.5,10.5))
  py.ylim((-1.5,3.5))
  py.savefig("images/one.png")

  py.figure(2)
  for method in l1errors.keys():
    for i in range(1,10):
      imax = 10 * 2**i
      data, l1 = calc_polytrope_butcher(1, method=method, analytic=n1_analytical, imax=imax)
      l1errors[method].append([10.0/(imax-1),l1])
    l1errors[method] = np.array(l1errors[method])
    tosolve = np.vstack([np.log(l1errors[method][2:,0]),np.ones(l1errors[method][2:,0].shape)]).T
    fit, res, rank, s = np.linalg.lstsq(tosolve, np.log(l1errors[method][2:,1]))
    py.loglog(l1errors[method][:,0],l1errors[method][:,1],
       label=r"%s, $ L1 \approx O \left( \Delta z^{ %0.2f } \right) $"%(method,fit[0]),
       c=cc.next(),marker=cm.next(),linestyle=cl.next())
    py.loglog(l1errors[method][:,0], l1errors[method][:,0]**fit[0]*np.exp(fit[1]))
  py.grid(True)
  py.xlim(xmax=1.25)
  py.title("L1 error for various RK methods")
  py.xlabel(r"$ \Delta z $")
  py.ylabel(r"$ L1( \Delta z ) $")
  py.legend(loc="lower right")
  py.savefig("images/two.png")

  py.figure(3)
  for n in (1., 3./2., 3.):
    data, l1 = calc_polytrope_butcher(n, method="rk4",imax=60,zmax=7.0)
    radius = find_radius(data)
    py.axvline(radius,color=(.9,)*3)
    py.plot(data[:,0],data[:,1],label="n = %0.1f, r=%0.2f"%(n,radius),c=cc.next(),marker=cm.next(),linestyle=cl.next())
  py.axhline(y=0,color=(.8,)*3)
  py.legend()
  py.xlabel("z")
  py.ylabel("w")
  py.title(r"$n \in \{1,\frac{3}{2},3\}$ Polytrope solved with RK4.")
  py.savefig("images/three.png")

  py.figure(4)
  py.subplot(211)
  roots = []
  for n in np.arange(0,5,0.05):
    data, l1 = calc_polytrope_butcher(n, method="rk4",imax=500,zmax=100.0)
    radius = find_radius(data)
    if radius != -1:
      roots.append([n,radius])
    py.axvline(radius,color=(.9,)*3)
    py.plot(data[:,0],data[:,1],label="n = %0.1f, r=%0.2f"%(n,radius))
  py.axhline(y=0,color=(.8,)*3)
  py.xlabel("z")
  py.ylabel("w")
  py.title("Profile of Polytrope for various polytropic indicies")
  py.ylim((-.25,1))
  py.xlim(xmin=0)

  py.subplot(212)
  roots = np.array(roots)
  from scipy.optimize import leastsq
  target = lambda x,p : p[0] * np.exp(x*p[1])+p[2]
  error = lambda p,x,y : y - target(x,p)
  x = leastsq(error, (1,1,1), (roots[:,0],roots[:,1]))[0]
  py.plot(roots[:,0],target(roots[:,0],x),label=r"$ r ( n ) = %0.2e \cdot e^{%0.2f \cdot n} + %0.2f $"%(x[0],x[1],x[2])) 
  py.plot(roots[:,0],roots[:,1], marker=cm.next())
  py.xlim((0,4.75))
  py.ylim((0,100))
  py.grid(True, which="both")
  py.xlabel("n")
  py.ylabel("radius")
  py.title("Radius vs Polytropic index")
  py.legend()
  py.savefig("images/four.png")
