#!/usr/bin/python

def primes(max):
	primes = [2]
	notprimes = []
	fac = lambda n:[1,0][n>0] or fac(n-1)*n

	for i in range(3, max+1,2):
		if not any(x % i for x in notprimes):
			if primality(i):
				primes.append(i)
			else
				notprimes.append(i)