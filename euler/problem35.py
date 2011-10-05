#!/usr/local/python

def find_primes(n):
        if n==2: return [2]
        elif n<2: return []
        s=range(3,n+1,2)
        mroot = n ** 0.5
        half=(n+1)/2-1
        i=0
        m=3
        while m <= mroot:
                if s[i]:
                        j=(m*m-3)/2
                        s[j]=0
                        while j<half:
                                s[j]=0
                                j+=m
                i=i+1
                m=2*i+3
        return [2]+[x for x in s if x]

def is_circular(n,primes):
	n = str(n)
	print n
	for i in range(len(n)):
		if int(n[i:] + n[:i]) not in primes:
			return False
	return True

primes = find_primes(1000000)
number=0
counter = 0
for i in primes:
	if counter % 10000 == 0:
		print counter/1000000.0, "%"
	i = str(i)
	circular = 1
	for n in range(len(i)):
		if int(i[n:] + i[:n]) not in primes:
			circular = 0
			break	
	number += circular
	counter+=1
print number