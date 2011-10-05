#!/usr/bin/python
import re, time

def isprime(n):
  if n%2==0:
    return False
  return not re.match(r'^1?$|^(11+?)\1+$', '1' * n)

fd = file("primes","w+")
starttime = time.clock()
i = 2
benchmark = []
while True:
  if isprime(i):
    fd.write("%d\n"%i)
  if i%500==0:
    timetaken = i/(time.clock()-starttime)
    benchmark.append([i,timetaken])
    print "Calculating at %d tests/s.  At i=%d"%(timetaken,i)
  i += 1
