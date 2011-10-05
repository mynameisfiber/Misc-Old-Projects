#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

typedef  unsigned long long bignum;

void printPrime(bignum bn)
	{
	static char buf[1000];

	sprintf(buf, "%ull", bn);
	buf[strlen(buf) - 2] = '\0';
	printf("%s\n", buf);
	}

void findPrimes(bignum topCandidate)
	{
	char *array = (char*)malloc(sizeof(unsigned char) * (topCandidate + 1));
	assert(array != NULL);

	/* SET ALL BUT 0 AND 1 TO PRIME STATUS */
	int ss;
	fprintf(stderr, "Making array\t\t");
	for(ss = 0; ss <= topCandidate+1; ss++)
		*(array + ss) = 1;
	fprintf(stderr, "[done]\n");
	array[0] = 0;
	array[1] = 0;

	/* MARK ALL THE NON-PRIMES */
	bignum thisFactor = 2;
	bignum lastSquare = 0;
	bignum thisSquare = 0;
	while(thisFactor * thisFactor <= topCandidate)
		{
		  fprintf(stderr, "Finding factors of %d\t\t", thisFactor);
		/* MARK THE MULTIPLES OF THIS FACTOR */
		bignum mark = thisFactor + thisFactor;
		while(mark <= topCandidate)
			{
			*(array + mark) = 0;
			mark += thisFactor;
			}

		/* PRINT THE PROVEN PRIMES SO FAR */
		thisSquare = thisFactor * thisFactor;
		for(;lastSquare < thisSquare; lastSquare++)
			{
			if(*(array + lastSquare)) printPrime(lastSquare);
			}

		/* SET thisFactor TO NEXT PRIME */
		thisFactor++;
		while(*(array+thisFactor) == 0) thisFactor++;
		assert(thisFactor <= topCandidate);
		fprintf(stderr, "[done]\n");
		}

	/* PRINT THE REMAINING PRIMES */
	for(;lastSquare <= topCandidate; lastSquare++)
		{
		if(*(array + lastSquare)) printPrime(lastSquare);
		}
	free(array);
	}

int main(int argc, char *argv[])
	{
	bignum topCandidate = 1000;
	if(argc > 1)
		topCandidate = atoll(argv[1]);
	findPrimes(topCandidate);
	return 0;
	}
