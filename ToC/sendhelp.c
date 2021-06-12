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
	
	// Stack allocation 
	int c;
	int d = 69;
	c = 25 + 20;
	c -= 5;
	
	char *e = (char*)malloc(13);
	if(e != NULL) memcpy(e, "Hello world!", 13);
	char *f = (char*)malloc(20);
	memcpy(f, "0123456789abcdefghi", 20);
	e = realloc(e, 26);
	memcpy(e, "Hello there! How are you?", 26);
	
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
	
	for (int __sts_loopcount_hDg = 0; __sts_loopcount_hDg < 10; __sts_loopcount_hDg++) {
		for (int __sts_loopcount_UFx = 0; __sts_loopcount_UFx < 10; __sts_loopcount_UFx++) {
			printf("ting");
		}
		
		printf("owo");
	}
	
	raiseException(104, "No Description provided");
	
	// Deleting variables 
	free(a)
	free(b)
	return 0;
}
