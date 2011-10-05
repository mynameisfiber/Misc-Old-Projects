#!/bin/env cython
#
# cybutcher: general RK solver using butcher tableau's.  This code uses
#            cython + numpy for speed and precision and maintains 64bit
#            accuracy throughout computation.  Performs one iteration
#            of RK4 in 64us on i7 290 CPU.
# author:    micha gorelick, gorelick@nyu.edu
# date:      30/09/10
#
# Refernce:  http://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods#Explicit_Runge.E2.80.93Kutta_methods

import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
def butcher(f, 
            np.ndarray v0, 
            t, 
            dt,
            np.ndarray tab,
            fargs = None):
  """f = function to be solved
     v0 = initial conditions
     t = physical time 
     dt = timestep
     tab = butcher tableau to be used
     fargs = additional arguments to be sent to f (optional)"""

  #First we define the variables we wish to use
  cdef int num_k = tab.shape[1]-1
  cdef int b_loc = tab.shape[0]-1
  cdef np.ndarray k = np.zeros((num_k,v0.shape[0]), dtype=DTYPE)
  cdef np.ndarray ak_i
  cdef np.ndarray v1 = np.array(v0, copy=True, dtype=DTYPE)

  #Now we solve!
  cdef unsigned int i
  for i from 0 <= i < num_k:
    # ak_i = sum(a_ij, k_j)
    ak_i = np.dot(tab[i,1:num_k+1],k)
    # k_i = f(t_n + c_i*dt, v_0 + sum(a_ij*k_j))
    k[i,:] = f( t + tab[i,0] * dt,
               v0 +     ak_i * dt,
               *fargs
              )
    # v1 = v0 + dt*sum(b_i * k_i)
    v1 += dt*tab[b_loc,i+1]*k[i]
  return v1,k

