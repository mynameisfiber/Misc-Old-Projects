
from numpy import pi, sqrt

def inject(u,center,I,rinj=5,MAXVEL=50):
  V = 4.0/3.0 * pi * (rinj**3)
  print "Injecting at", center
  for x in range(center[0]-rinj,center[0]+rinj+1):
    for y in range(center[1]-rinj,center[1]+rinj+1):
      for z in range(center[2]-rinj,center[2]+rinj+1):
        r = sqrt((x-center[0]+.5)**2 + (y-center[1]+.5)**2 + (z-center[2]+.5)**2)
        if r <=  rinj and within([0,0,0],[x,y,z],u.shape[1:]):
          try:
            #u[0,x,y,z] += (I/V)/MAXVEL
            u[1,x,y,z] += I/V * (x-center[0]+.5)/r
            u[2,x,y,z] += I/V * (y-center[1]+.5)/r
            u[3,x,y,z] += I/V * (z-center[2]+.5)/r
          except IndexError:
            pass
  return u

def within(l,m,h):
  assert(len(l) == len(m) == len(h))
  for i in range(len(m)):
    if not l[i] <= m[i] < h[i]:
      return False
  return True
