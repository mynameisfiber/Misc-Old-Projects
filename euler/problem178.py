#!/usr/bin/python

def pandigital(n):
        n = str(n)
        for i in range(0,len(n)+1):
                if str(i) not in n:
                        return 0
        return 1

def stepNumber(n, d):
	if d==len(n): return 0
	counter = 0
	print n[:d] + str(int(n[d:d+1])+1) + n[d+1:]
	print n[:d] + str(int(n[d:d+1])-1) + n[d+1:]
	counter += pandigital(n[:d] + str(int(n[d:d+1])+1) + n[d+1:]) + stepNumber(n[:d] + str(int(n[d:d+1])+1) + n[d+1:], d+1)
	counter += pandigital(n[:d] + str(int(n[d:d+1])-1) + n[d+1:]) + stepNumber(n[:d] + str(int(n[d:d+1])-1) + n[d+1:], d+1)
	counter += stepNumber(n[:d] + str(int(n[d:d+1])) + n[d+1:], d+1)
	return counter

print stepNumber("111",0)
		