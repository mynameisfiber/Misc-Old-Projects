#!/usr/bin/python

import numpy, sys
n = int(sys.argv[1]) if len(sys.argv) > 2 else 50
u = numpy.zeros((4,n,n,n))
u[0,:,:,:] = 1


from tvd import tvd
