#!/usr/bin/python
import sys

sum = 0
last = -10000
negative = 1
try:
  accuracy = 10**-(float(sys.argv[1])+1)
except IndexError:
  print "Usage: %s [n] where the result is accurate within n decimal places"
  exit(1)

i = 1.0
while abs(last-sum)>accuracy or negative == 1:
  last = sum
  sum += negative * 1./i
  negative *= -1
  i += 2

print sum*4
print "%d iterations"%( (i-1)/2)
