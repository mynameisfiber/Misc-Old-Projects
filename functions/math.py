#!/usr/bin/python
#Set of helper functions for math's.

def order(a,m=24):
  """Return the order of element a in the group Z_n={0,1,...,n-1} under addition modulo n"""
  assert(1 < a < m)
  for k in range(2,m):
    if a*k % m == 0:
      return k
  return 0
  
def gcd(a,b):
  """Return greatest common divisor using Euclid's Algorithm."""
  while b:      
    a, b = b, a % b
  return a

