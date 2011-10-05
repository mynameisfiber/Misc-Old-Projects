#!/usr/bin/python
#made by mg

import sys

try:
  import psyco
  psyco.full()
except ImportError:
  print "PsYco not availible"

def primes(n):
	""" returns a list of prime numbers from 2 to < n """
	if n < 2: return []
	if n == 2: return [2]
	s = range(3, n, 2)
	mroot = n ** 0.5
	half = len(s)
	i = 0
	m = 3
	while m <= mroot:
		if s[i]:
			j = (m * m - 3)//2
			s[j] = 0
			while j < half:
				s[j] = 0
				j += m
		i = i + 1
		m = 2 * i + 3
	return [2]+[x for x in s if x]

if len(sys.argv) != 2:
	print "Usage: " + sys.argv[0] + " [max]"
else:
	print primes(int(sys.argv[1]))
