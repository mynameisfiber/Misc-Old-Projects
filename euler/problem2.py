#!/usr/local/python
"""Find the sum of all the even-valued terms in the sequence which do not exceed four million."""

x=1
y=2
temp=0
sum = 0

while y <= 4000000:
	if y % 2 == 0:
		sum += y
	temp = x+y
	x = y
	y = temp
print y
print sum		
