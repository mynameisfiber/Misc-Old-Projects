#!/usr/bin/python

import sys,math

def primes(n):
	""" returns a list of Mersenne prime numbers from 2 to < n """
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
	log2 = math.log(2)
	return [x for x in s if x and not math.log(x+1)/log2%1]

if len(sys.argv) <> 2:
	print "Prints Mersenne Primes from 2 < n < max"
	print "Usage: " + sys.argv[0] + " [max]"
else:
	print primes(int(sys.argv[1]))
