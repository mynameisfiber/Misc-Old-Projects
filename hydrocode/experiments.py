from hllrkfluxlimit import hllrkfluxlimit
from hllrk import hllrk
from hlleuler import hlleuler
from hllrkfluxlimit2d import hllrkfluxlimit2d
from hllrk2d import hllrk2d
from hlleuler2d import hlleuler2d

import cPickle
import numpy as np
import pylab as py
from sys import stdout
import os
from os.path import splitext

####PARAMETERS#####
gamma = 1.4
dx    = 0.1
dy    = 0.1
CFL   = 0.4
theta = 1.5
###################

experiments = {}
experiments[1] = [{"name":splitext(fname)[0],"u":cPickle.load(file("data/%s"%fname))} for fname in ("shock1d.dat",)]
experiments[2] = [{"name":splitext(fname)[0],"u":cPickle.load(file("data/%s"%fname))} for fname in ("shock2d-vertical.dat",
                                                                                                    "shock2d-horizontal.dat",
                                                                                                    "shock2d-circle.dat",
                                                                                                    "helmholtz2d-slow.dat", 
                                                                                                    "helmholtz2d-fast.dat")]

solvers = {}
solvers[1] = [{"name":"hlleuler","object":hlleuler,"init":(gamma,dx,CFL)},
              {"name":"hllrk","object":hllrk,"init":(gamma,dx,CFL)},
              {"name":"hllrkfluxlimit","object":hllrkfluxlimit,"init":(gamma,dx,CFL,theta)}]
solvers[2] = [{"name":"hlleuler","object":hlleuler2d,"init":(gamma,dx,dy,CFL)},
              {"name":"hllrk","object":hllrk2d,"init":(gamma,dx,dy,CFL)},
              {"name":"hllrkfluxlimit","object":hllrkfluxlimit2d,"init":(gamma,dx,dy,CFL,theta)}]

def plotSetup(u, d, expname, solname):
  plot = {}
  try:
    os.makedirs("images/%s/%s"%(solname,expname))
  except:
    pass
  plot["figure"] = py.figure(figsize=(9,9))
  plot["title"] = plot["figure"].suptitle("tmp",fontsize=18)
  if d == 2:
    py.subplot(221)
    py.title(r"$density$")
    plot["density"] = py.imshow(u[:,:,0])
    py.subplot(222)
    py.title(r"$velocity_x$")
    plot["vx"] = py.imshow(u[:,:,1])
    py.subplot(223)
    py.title(r"$velocity_y$")
    plot["vy"] = py.imshow(u[:,:,2])
    py.subplot(224)
    py.title(r"$Energy$")
    plot["e"] = py.imshow(u[:,:,3])
  elif d == 1:
    plot["density"] = py.plot(u[:,0],label="density")[0]
    plot["v"] = py.plot(u[:,1]/u[:,0],label="velocity")[0]
    plot["e"] = py.plot(u[:,2],label="energy")[0]
    py.legend()
  return plot

def plotTimestep(plot, u, i, d, t, expname, solname):
  plot["title"].set_text("%s on %s at t=%0.2f"%(solname, expname,t))
  if d == 2:
    plot["density"].set_array(u[:,:,0])
    plot["density"].autoscale()
    plot["vx"].set_array(u[:,:,1]/u[:,:,0])
    plot["vx"].autoscale()
    plot["vy"].set_array(u[:,:,2]/u[:,:,0])
    plot["vy"].autoscale()
    plot["e"].set_array(u[:,:,3])
    plot["e"].autoscale()
  elif d == 1:
    plot["density"].set_ydata(u[:,0].copy())
    plot["v"].set_ydata(u[:,1]/u[:,0])
    plot["e"].set_ydata(u[:,2].copy())
  py.draw()
  py.savefig("images/%s/%s/%s-%s-%0.5d.png"%(solname,expname,solname,expname,i))
  return plot


def runExperiment(solver, experiment, d):
  print "Running experiment %s with %s"%(experiment["name"], solver["name"])
  solver["object"].init(*solver["init"])
  i = 0
  u = experiment["u"].copy()
  plot = plotSetup(u,d, experiment["name"], solver["name"])
  dt = 0.05
  lastt = 0.0
  try:
    while lastt <= 20:
      u = solver["object"].step(u)
      if solver["object"].t - lastt >= dt:
        print "\tPlotting t=%4.2f\r"%lastt,
        stdout.flush()
        lastt += dt
        plot = plotTimestep(plot, u, i, d, solver["object"].t, experiment["name"], solver["name"])
      i += 1
  except:
    pass
  print "\n\tAnimating"
  os.system(r"mencoder -msglevel all=-1 mf://images/%s/%s/*.png -mf fps=20:type=png -ovc lavc -lavcopts vcodec=mpeg4 -oac copy -o videos/%s-%s.avi -ffourcc DX50"%(solver["name"],experiment["name"],solver["name"],experiment["name"]))

for d,experimentd in experiments.iteritems():
  for experiment in experimentd:
    for solver in solvers[d]:
      runExperiment(solver, experiment, d)

