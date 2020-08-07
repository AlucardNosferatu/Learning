#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct alist {
	int n;
	int maxsize;
	int *table;
} Alist;
typedef struct alist* ListA;

typedef struct blist {
	int element;
	Blist* next;
} Blist;

typedef struct blist* ListB;


ListA ListInit(int size) {
	ListA list_p = malloc(sizeof(Alist));
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

ListB ListInit() {
	ListB list_p = malloc(sizeof(Blist));
	if (list_p) {
		return list_p;
	}
	else {
		return NULL;
	}
}

int ListEmpty(ListA L) {
	if (L) {
		if (L->n == 0) {
			return 0;
		}
		else {
			return 1;
		}
	}
	else {
		return 0;
	}
}

int ListLength(ListA L) {
	if (L) {
		return L->n;
	}
	else {
		return 0;
	}
}

int ListRetrieve(int k, ListA L) {
	if (L) {
		if (ListLength(L) == 0) {
			return -1;
		}
		else {
			return L->table[k];
		}
	}
	else {
		return -1;
	}
}

int ListLocate(int x, ListA L) {
	if (L) {
		if (ListLength(L) == 0) {
			return -1;
		}
		else {
			int length = L->n;
			for (int i = 0; i < length; i++) {
				if (L->table[i] == x) {
					return i;
				}
			}
			return -1;
		}
	}
	else {
		return -1;
	}
}

void ListInsert(int k, int x, ListA L) {
	if (L) {
		int length = L->n;
		if (length == 0) {
			L->table[0] = x;
			L->n = length + 1;
		}
		else if ((0 <= k) && (k < length) && (length < (L->maxsize))) {
			for (int i = length; i > k; i--) {
				L->table[i] = L->table[i - 1];
			}
			L->table[k] = x;
			L->n = length + 1;
		}
	}
}

int ListDelete(int k, ListA L) {
	if (L) {
		int length = L->n;
		if ((0 <= k) && (k < length)) {
			int temp = L->table[k];
			for (int i = k; i < length; i++) {
				if ((i + 1) < L->maxsize) {
					L->table[i] = L->table[i + 1];
				}
			}
			L->n = length - 1;
			return temp;
		}
		else {
			return -1;
		}
	}
	else {
		return -1;
	}
}

void PrintList(ListA L) {
	if (L) {
		int length = L->n;
		for (int i = 0; i < length; i++) {
			printf("%d", L->table[i]);
			printf(" ");
		}
		printf(" End of Table\n");
	}
}

void main_LinearTable() {
	ListA L = ListInit(10);
	PrintList(L);
	ListInsert(0, 5, L);
	ListInsert(0, 7, L);
	ListInsert(0, 2, L);
	PrintList(L);
	int temp = ListDelete(1, L);
	ListInsert(1, 11, L);
	PrintList(L);
	temp = ListDelete(0, L);
	PrintList(L);
	printf("%d", ListEmpty(L));
}