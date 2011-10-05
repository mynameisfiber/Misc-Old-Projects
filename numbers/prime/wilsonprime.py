#!/usr/bin/python

import math
import sys

def fac(x):
	sum = 1
	for i in range(1,x+1):
		sum *= i
	return sum

for i in range(1,int(sys.argv[1])):
#	print "\t", i
#	print "\t", fac(i)
	x = 2 + 2 * fac(i) % (i+1)
