#!/bin/local/python
"""Find the largest palindrome made from the product of two 3-digit numbers."""

def reverseString(s):
    """Reverses a string given to it."""
    return s[::-1]

interate=range(100,999)
interate.reverse()
largest=0
for i in interate:
	for j in interate:
		test = i * j
		if reverseString(str(test)[:3]) == str(test)[3:]:
			if test > largest:
				print "Found: ", test
				largest = test

print "Largest: ", largest
		

