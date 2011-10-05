from hllrkfluxlimit import hllrkfluxlimit
from hllrk import hllrk
from hlleuler import hlleuler
import cPickle
import numpy as np
import pylab as py

u = cPickle.load(file("1dshock.dat","r"))

urkfl = u.copy()
urk = u.copy()
ueuler = u.copy()

gamma = 1.4
hllrkfluxlimit.init(gamma, 0.01, 0.8,1.5)
hllrk.init(gamma, 0.01, 0.8)
hlleuler.init(gamma, 0.01, 0.8)

py.ion()

def make_plot_array(u):
  plots = []
  plots.append(py.plot(u[:,0],label="density")[0])
  plots.append(py.plot(u[:,1]/u[:,0],label="velocity")[0])
  plots.append(py.plot(u[:,2],label="energy")[0])
  return plots

def update_plot(plots,u):
  plots[0].set_ydata(u[:,0].copy())
  plots[1].set_ydata(u[:,1]/u[:,0])
  plots[2].set_ydata(u[:,2].copy())
  return plots

py.figure(figsize=(12,12))
py.subplot(311)
plotrkfl = make_plot_array(urkfl)
py.legend()

py.subplot(312)
plotrk = make_plot_array(urk)
py.legend()

py.subplot(313)
ploteuler = make_plot_array(ueuler)
py.legend()

dt = 0.05
tlast = 0
while True:
  if hllrkfluxlimit.t < tlast + dt:
    urkfl  = hllrkfluxlimit.step(urkfl)
  elif hllrk.t < tlast + dt:
    urk    = hllrk.         step(urk)
  elif hlleuler.t < tlast + dt:
    ueuler = hlleuler.     step(ueuler)
  else:
    py.subplot(311)
    py.title("RK Flux Limited @ t=%0.2f"%hllrkfluxlimit.t)
    plotrkfl = update_plot(plotrkfl, urkfl)

    py.subplot(312)
    py.title("RK @ t=%0.2f"%hllrk.t)
    plotrk = update_plot(plotrk, urk)

    py.subplot(313)
    py.title("Euler @ t=%0.2f"%hlleuler.t)
    ploteuler = update_plot(ploteuler, ueuler)

    py.draw()

    tlast += dt
