#!/usr/local/python

"""Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum."""

sumSquares=0
squareSum=0
for i in range(1,101):
	sumSquares+=i*i
	squareSum+=i

print squareSum*squareSum,sumSquares
print (squareSum*squareSum-sumSquares)