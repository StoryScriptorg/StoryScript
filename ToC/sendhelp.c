#include <stdio.h>
#include <stdlib.h>

int main() {
	// Heap allocation 
	int *a = (int*)malloc(sizeof(int));
	int *b = (int*)malloc(sizeof(int));
	*b = 10;
	
	// Stack allocation 
	int c;
	int d = 69;
	
	printf("Hello world");
	switch (d)
	{
		case 10:
			break;
		case 69:
			break;
	}
	
	for (int __sts_loopcount_yYJ = 0; __sts_loopcount_yYJ < 10; __sts_loopcount_yYJ++) {
		for (int __sts_loopcount_tBy = 0; __sts_loopcount_tBy < 10; __sts_loopcount_tBy++) {
			printf("ting");
		}
		
		printf("owo");
	}
	
	
	// Deleting variables 
	free(a)
	free(b)
	return 0;
}
