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
	struct blist* next;
} Blist;
typedef struct blist* ListB;

typedef struct clist {
	int n;
	int maxsize;
	int** table;
} Clist;
typedef struct clist* ListC;


ListA ListInitA(int size) {
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

ListB ListInitB() {
	ListB list_p = malloc(sizeof(Blist));
	if (list_p) {
		list_p->element = 0;
		list_p->next = NULL;
		return list_p;
	}
	else {
		return NULL;
	}
}

ListC ListInitC(int size) {
	ListC list_p = malloc(sizeof(Clist));
	if (list_p) {
		list_p->maxsize = size;
		list_p->n = 0;
		list_p->table = malloc(list_p->maxsize * sizeof(int*));
		if (list_p->table) {
			memset(list_p->table, NULL, (list_p->maxsize * sizeof(int*)));
			return list_p;
		}
		else {
			return NULL;
		}
	}
	else {
		return NULL;
	}
}

int ListEmptyA(ListA L) {
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

int ListEmptyB(ListB L) {
	if (L) {
		if ((L->next) && (L->element)) {
			return 1;
		}
		else {
			return 0;
		}
	}
	else {
		return 0;
	}
}

int ListEmptyC(ListC L) {
	return L->n == 0;
}

int ListLengthA(ListA L) {
	if (L) {
		return L->n;
	}
	else {
		return 0;
	}
}

int ListLengthB(ListB L) {
	if (L) {
		int count = 0;
		while (L) {
			if (L->element) {
				count += 1;
				if (L->next) {
					L = L->next;
				}
				else {
					return count;
				}
			}
			else {
				break;
			}
		}
		return count;
	}
	else {
		return -1;
	}
}

int ListLengthC(ListC L) {
	if (L) {
		return L->n;
	}
	else {
		return 0;
	}
}

int ListRetrieveA(int k, ListA L) {
	if (L) {
		if (ListLengthA(L) == 0) {
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

int ListRetrieveB(int k, ListB L) {
	if (L) {
		for (int i = 0; i < k; i++) {
			if (L->next) {
				L = L->next;
			}
			else {
				return 0;
			}
		}
		if (L->element) {
			return L->element;
		}
		else {
			return 0;
		}
	}
	else {
		return 0;
	}
}

int ListRetrieveC(int k, ListC L) {
	return *(L->table[k]);
}

int ListLocateA(int x, ListA L) {
	if (L) {
		if (ListLengthA(L) == 0) {
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

int ListLocateB(int x, ListB L) {
	if (L) {
		int index = 0;
		while (L) {
			if (L->element) {
				if (L->element == x) {
					return index;
				}
				else {
					if (L->next) {
						L = L->next;
						index += 1;
					}
					else {
						return -1;
					}
				}
			}
			else {
				return -1;
			}
		}
		return -1;
	}
	else {
		return -1;
	}
}

int ListLocateC(int x, ListC L) {
	for (int i = 0; i < L->n; i++) {
		if (*(L->table[i]) == x) {
			return i;
		}
	}
	return -1;
}

void ListInsertA(int k, int x, ListA L) {
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

void ListInsertB(int k, int x, ListB L) {
	if (L) {
		ListB nextL = malloc(sizeof(Blist));
		if (nextL) {
			if (k > 0) {
				nextL->element = x;
				for (int i = 0; i < (k - 1); i++) {
					L = L->next;
				}
				nextL->next = L->next;
				L->next = nextL;
			}
			else if (k == 0) {
				nextL->element = L->element;
				L->element = x;
				nextL->next = L->next;
				L->next = nextL;
			}
		}
	}
}

void ListInsertC(int k, int x, ListC L) {
	for (int i = L->n + 1; i > k; i--) {
		L->table[i] = L->table[i - 1];
	}
	L->table[k] = malloc(sizeof(int));
	if (L->table[k]) {
		*(L->table[k]) = x;
	}
	L->n += 1;
}

int ListDeleteA(int k, ListA L) {
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

int ListDeleteB(int k, ListB L) {
	if (L) {
		if (k > 0) {
			for (int i = 0; i < k - 1; i++) {
				L = L->next;
			}
			int temp = L->next->element;
			ListB deleted = L->next;
			L->next = L->next->next;
			free(deleted);
			return temp;
		}
		else if (k == 0) {
			int temp = L->element;
			L->element = L->next->element;
			ListB deleted = L->next;
			L->next = L->next->next;
			free(deleted);
			return temp;
		}
		else {
			return 0;
		}
	}
	else {
		return 0;
	}
}

int ListDeleteC(int k, ListC L) {
	int temp = *(L->table[k]);
	for (int i = k; i < L->n-1; i++) {
		L->table[i] = L->table[i + 1];
	}
	L->table[L->n - 1] = NULL;
	L->n -= 1;
	return temp;
}

void PrintListA(ListA L) {
	if (L) {
		int length = L->n;
		for (int i = 0; i < length; i++) {
			printf("%d", L->table[i]);
			printf(" ");
		}
		printf(" End of Table\n");
	}
}

void PrintListB(ListB L) {
	if (L) {
		while (L) {
			if(L->element){
				printf("%d", L->element);
				printf(" ");
			}
			L = L->next;
		}
		printf(" End of Table\n");
	}
}

void main_LinearTable() {
	ListC L = ListInitC(10);
	ListInsertC(0, 24, L);
	ListInsertC(0, 12, L);
	ListInsertC(0, 2029, L);
	ListDeleteC(1, L);
}