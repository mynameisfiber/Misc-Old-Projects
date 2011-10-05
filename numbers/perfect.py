#!/usr/bin/python

import sys,math

def perfect(n):
	""" returns a list of perfect numbers by finding Mersenne prime numbers from 2 to < n """
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
	return [((2**(math.log(x+1)/log2)-1)*2**(math.log(x+1)/log2-1)) for x in s if x and not math.log(x+1)/log2%1]

if len(sys.argv) <> 2:
	print "Prints perfect numbers by finding Mersenne Primes from 2 < n < max"
	print "Usage: " + sys.argv[0] + " [max]"
else:
	print perfect(int(sys.argv[1]))
