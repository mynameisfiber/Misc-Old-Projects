#!/usr/bin/python
"""Find the sum of all the multiples of 3 or 5 below 1000."""

sum=0
y=3

while y<1000:
	if y % 3 == 0 or y % 5 == 0:
		sum+=y
	y+=1
print sum
