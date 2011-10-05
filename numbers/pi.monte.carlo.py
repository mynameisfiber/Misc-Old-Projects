#!/usr/bin/python

resolution=500
inside=0.0

for x in range(resolution):
	for y in range(resolution):
		if y == 0 and x%10==0:
			print (x * 100 / resolution), "% done"
		if (x**2 + y**2) < resolution**2:
			inside+=1
pi = 4.0 * inside / resolution**2

print "Points used: ", resolution**2
print "Calculated PI: ", pi