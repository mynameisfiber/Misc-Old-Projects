#!/usr/bin/python

import numpy
from tvd import tvd

class rotating-grid:
  def __init__(self, u, center, dtheta, CFL=0.65):
    self.u = u
    self.center = center
    self.dtheta = dtheta
    self.theta = 0
    self.CFL = CFL
    self.dt = 0
    self.maxv = 0

  def step():
    self.u, self.dt, self.maxv = tvd.step(self.u, self.CFL)
    self.rotate_grid(self.dtheta, self.dt)
   
  def rotate_grid(dtheta, dt):
    self.theta = dt * dtheta
    newu = self.u.copy()
    for z in xrange(self.u.shape[2]):
      for y in xrange(self.u.shape[1]):
        for x in xrange(self.u.shape[0]):
          r = sqrt(x*x + y*y + z*z)
          newu[x,y,z] = get_cell_average(r,
