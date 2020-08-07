#include <stdio.h>
#include <stdlib.h>

typedef struct alist {
	int n;
	int maxsize;
	int *table;
} Alist;

typedef struct alist* List;

List ListInit(int size) {
	List list_p = malloc(sizeof(Alist));
	if (list_p) {
		list_p->maxsize = size;
		list_p->n = 0;
		list_p->table = malloc(list_p->maxsize * sizeof(int));
		return list_p;
	}
	else {
		return NULL;
	}
}

void main_LinearTable() {
	printf("Hello World");
}