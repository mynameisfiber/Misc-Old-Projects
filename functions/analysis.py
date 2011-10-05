#!/bin/env python
from __future__ import division

def power_spectrum2D(x, dk=1):
  #Method taken from:
  # Abramenko, V.I.. Relationship between magnetic power spectrum and flare
  #   productivity in solar active regions Astrophys. J., 629, 1141-1149, 2003
  #   (http://www.bbso.njit.edu/~avi/PowerSp.pdf)
  assert( len(x.shape) == 2 )
  assert( x.shape[0] == x.shape[1] )
  from numpy import fft
  import numpy
  U = fft.fftn(x)
  F = U * U.conj()
  maxradius = numpy.round(F.shape[0]*numpy.sqrt(2) / dk) + 1
  k = (numpy.arange(maxradius) + .5) * dk
  E = numpy.zeros(maxradius)
  for x in range(F.shape[0]):
    x2 = x*x
    for y in range(F.shape[1]):
      y2 = y*y
      distance = numpy.sqrt(x2 + y2)
      try:
        E[int(numpy.fix(distance/dk))] += F[x,y]
      except:
        print int(numpy.fix(distance/dk)), len(E), x, y
  return E/(8*numpy.pi*dk), k
  
def load_slice(i,dir,ovars):
  width = int(ovars['procs'] ** (1.0/3.0))+1
  rho =   numpy.zeros((ovars['gsize']+1,ovars['gsize']+1,width))
  rhovx = numpy.zeros((ovars['gsize']+1,ovars['gsize']+1,width))
  rhovy = numpy.zeros((ovars['gsize']+1,ovars['gsize']+1,width))
  rhovz = numpy.zeros((ovars['gsize']+1,ovars['gsize']+1,width))
  isint = lambda x : x == int(x)
  for n in range(ovars['procs']):
    fd = open(dir+"output-slice-%.8d-%.3d"%(i,n))
    a,b,c,d = numpy.fromfile(file=fd,dtype=numpy.float32).reshape((ovars['size'],ovars['size'],4)).T
    offset_mpi = numpy.fromfile(file=open(dir+"output-offset-%.3d"%n),dtype=numpy.int32)
    offset = [0,0,0]
    offset[0] = (int(offset_mpi[1]*ovars['size']), int((offset_mpi[1]+1)*ovars['size']))
    offset[1] = (int(offset_mpi[2]*ovars['size']), int((offset_mpi[2]+1)*ovars['size']))
    offset[2] = offset_mpi[0]

    rho  [offset[0][0]:offset[0][1], offset[1][0]:offset[1][1], offset[2]] = a
    rhovx[offset[0][0]:offset[0][1], offset[1][0]:offset[1][1], offset[2]] = b
    rhovy[offset[0][0]:offset[0][1], offset[1][0]:offset[1][1], offset[2]] = c
    rhovz[offset[0][0]:offset[0][1], offset[1][0]:offset[1][1], offset[2]] = d
          
    fd.close()
  return (rho,rhovx,rhovy,rhovz)

  
def loadparams(dir):
  ovars = {}
  try:
    for line in file(dir+"params.f90").readlines():
      vars = re.search("[^!]+[ \t]*(REAL|INTEGER), [\w]* :: ([\w]*)[ ]?=[ ]?([.\-0-9e]*)", line)
      if vars is not None:
        if vars.group(1) == "REAL":
          ovars[vars.group(2)] = float(vars.group(3))
        elif vars.group(1) == "INTEGER":
          ovars[vars.group(2)] = int(vars.group(3))
    ovars['tmerge'] = ovars['op']**(3/7) / (ovars['oImp']**(3/7) * ovars['oSnorm0']**(4/7))
    ovars['lmerge'] = (ovars['oImp'] / (ovars['op'] * ovars['oSnorm0']))**(1/7)
    ovars['vchar'] = ovars['oImp']**(4/7) * ovars['oSnorm0']**(3/7) / ovars['op']**(4/7)
    ovars['size'] = ovars['n'] - 2*ovars['ghost']
    ovars['gsize'] = ovars['size'] * ovars['procs']**(1/3)
    return ovars
  except IOError:
    return None
    
def findIndex(needle, haystack):
  mindiff = numpy.inf
  for i,element in enumerate(haystack):
    if abs(element - needle) < mindiff:
      optimal = i
      mindiff = abs(element - needle)
  return optimal

if __name__ == "__main__":
  import sys
  import pylab
  import re
  import numpy
  
  assert( len(sys.argv) >= 3 )
  dir = sys.argv[1]
  odir = sys.argv[2]
  try:
    dk = int(sys.argv[3])
  except:
    dk = 1

  ovars = loadparams(dir)
  timesslice = numpy.transpose([[float(i) for i in x.strip().split()] for x in file(dir+"output-times-slice").readlines()])
  timesslice = dict([(timesslice[1][i],timesslice[0][i]) for i in range(len(timesslice[0]))])

  findstep = 4
  minstep = numpy.inf
  for step, time in timesslice.items():
    if abs(time/ovars['tmerge'] - findstep) < minstep:
      minstep = time/ovars['tmerge'] - findstep
      mergestep = step
  
  rho, rhovx, rhovy, rhovz = load_slice(mergestep, dir, ovars)
  rhov2 = rhovx[:,:,0]**2 + rhovy[:,:,0]**2 + rhovz[:,:,0]**2
  
  e,k = power_spectrum2D(rhov2, dk=dk)
  a = findIndex(ovars['lmerge'], k)
  b = findIndex(ovars['gsize']/2, k)
  fit = numpy.polyfit(numpy.log10(k[a:b]), numpy.log10(e[a:b]),1)
  
  pylab.loglog(k,e)
  pylab.axvline(ovars['lmerge'],linestyle=":")
  pylab.loglog(k[a:b], 11**(fit[1]) * (k[a:b] ** fit[0]), label=r"$ \beta = %0.2f $"%abs(fit[0]))
  pylab.xlabel(r"$ \frac{k}{k_{min}} $")
  pylab.ylabel(r"$ P \left( v_{ rms }^2 \right) $")
  pylab.title(r"Energy Spectrum at $ t = %d \cdot t_{merge} $"%(timesslice[mergestep]/ovars['tmerge']))
  pylab.legend()
  pylab.xlim(k[0],ovars['gsize']/2)
  pylab.savefig(odir+"/powerspec-%.8d.png"%mergestep)

