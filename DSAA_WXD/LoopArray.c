#include <stdio.h>
#include <stdlib.h>

typedef struct LoopArray {
	int n;
	int maxsize;
	int* table;
} LArray;
typedef LArray* LA_P;

LA_P InitLA(int size) {
	LA_P L = malloc(sizeof(LArray));
	if (L) {
		L->maxsize = size;
		L->n = 0;
		L->table = malloc(L->maxsize * sizeof(int));
		return L;
	}
	else {
		return NULL;
	}
}

int ConvertIndex(int index, LA_P L) {
	while (index >= L->n) {
		index -= L->n;
	}
	return index;
}
