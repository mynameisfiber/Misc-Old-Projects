#!/usr/bin/python
#this program takes input x and returns y,z such that:
#	x = y * z
#	y+z is minamized
#	y>=z
#the pair y,z shall be called the leastproduct

import math, sys

def findleastproduct(x):
	y = int(x**.5 + .5) 
	z = int(x**.5)
	while y*z != x and z != 0:
		if x< y*z:
			z-=1
		else:
			y+=1
	return (y,z)

if len(sys.argv) != 2:
	print "This finds the least product of input integer x (see program comments)"
	print "Usage: " + sys.argv[0] + " [x]"
else:
	print findleastproduct(int(sys.argv[1]))
