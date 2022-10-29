#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>

inline double rand01()
{
	return (double)rand() / RAND_MAX;
}

double getpi()
{
	int M = 0;                   
	int N = 400000;              
	for (int j = 0; j < N; j++) {
		double x = rand01();     
		double y = rand01();     
		if (x*x + y*y < 1) M++;  
	}                            
	double pi = (double)M / N * 4;
	return pi;
}

int main()
{
	// we guess the RNG: 
	// time() on server: backward from local case
	// clock() spent on server: 1500+-
	int rngmiddle = 1500 + (unsigned)time(0);
	printf("%d\n", rngmiddle);
	int maxjitter = 10000;
	
	// from first two failed guesses, 
	// derive the random seed
	double pi1, pi2;
	char guess[10];
	fgets(guess, 10, stdin);
	sscanf(guess, "%lf", &pi1);
	fgets(guess, 10, stdin);
	sscanf(guess, "%lf", &pi2);

	int sig = 1;
	for (int i = 0; i < maxjitter; i++) {
		printf("%d: ", i/2 * sig);
		srand(rngmiddle + i/2 * sig);
		double pitest1 = getpi();
		double pitest2 = getpi();
		double diff1 = fabs(pitest1 - pi1);
		double diff2 = fabs(pitest2 - pi2);
		if (diff1 < 1e-6 && diff2 < 1e-6) {
			printf("Match!\n");
			double pi3 = getpi();
			double pi4 = getpi();
			double pi5 = getpi();
			printf("%1.5f, %1.5f, %1.5f\n", pi3, pi4, pi5);
			break;
		}
		else
			printf("%1.5f %1.5f\n", diff1, diff2);
		sig = sig * -1;
	}
	return 0;
}
