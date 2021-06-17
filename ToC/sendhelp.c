#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Exception Raising
void raiseException(int code, char* description)
{
	switch(code)
	{
		case 100:
			printf("InvalidSyntax: %s", description);
			break;
		case 101:
			printf("AlreadyDefined: %s", description);
			break;
		case 102:
			printf("NotImplementedException %s", description);
			break;
		case 103:
			printf("NotDefinedException: %s", description);
			break;
		case 104:
			printf("GeneralException: %s", description);
			break;
		case 105:
			printf("DivideByZeroException: %s", description);
			break;
		case 106:
			printf("InvalidValue: %s", description);
			break;
		case 107:
			printf("InvalidTypeException: %s", description);
			break;
	}
	exit(code);
}

int main() {
	// Heap allocation 
	int *a = (int*)malloc(sizeof(int));
	int *b = (int*)malloc(sizeof(int));
	*b = 10;
	*a = 20;
	
	int float;
	
	// Stack allocation 
	int c;
	int d = 69;
	c = 25 + 20;
	c -= 5;
	
	char e[13] = "Hello world!";
	char *f = (char*)malloc(20);
	f = realloc(f, 37);
	memcpy(f, "0123456789abcdefghijklmnopqrstuvwxyz", 37);
	memcpy(e, "Hello there!", 13);
	
	// Dynamics 
	void* g = malloc(13);
	g = (void*)"Hello there!";
	void* h = (void*)75;
	h = (void*)500;
	
	printf("Hello world");
	switch (d)
	{
		case 10:
			printf("The value of d is 10");
			break;
		case 69:
			printf("**SIXTYNINE**");
			break;
	}
	
	for (int __sts_loopcount_JCW = 0; __sts_loopcount_JCW < 10; __sts_loopcount_JCW++) {
		for (int __sts_loopcount_NQc = 0; __sts_loopcount_NQc < 10; __sts_loopcount_NQc++) {
			printf("ting");
		}
		
		printf("owo");
	}
	
	if (d >= 60 && d < 70)
	{
		if (d == 69)
		{
			printf("The value of d is 69");
		} else {
			printf("The value of d is more than or equal to 60 and less than 70.");
		}
		
	} else {
		printf("The value of d is not more than or equal to 60 and less than 70.");
	}
	
	raiseException(104, "No Description provided");
	
	// Deleting variables 
	free(a);
	free(b);
	free(f);
	
	printf("spam ig");
	return 0;
}
