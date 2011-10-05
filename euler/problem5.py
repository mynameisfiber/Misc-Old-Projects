#!/bin/local/python
"""What is the smallest number that is evenly divisible by all of the numbers from 1 to 20?"""


test= 0
found=1

while found != 0:
	test += 20
	found = 0
	for i in range(1,20):
		found += test % i
	print "Tested: ", test, "Remainder of: ", found
		
print test
