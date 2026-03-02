#include <stdio.h>
#include <stdlib.h>

typedef struct node {
	int value;
	struct node* next;
	struct node* prev;
} Node;

typedef struct node_f {
	struct node* next;
} NodeF;

typedef struct node* NodeP;

typedef struct node_f* NodeFP;