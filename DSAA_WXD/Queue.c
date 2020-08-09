#include <stdio.h>
#include <stdlib.h>

typedef struct aqueue {
	int element;
	struct aqueue* next;
} AQueue;
typedef struct first_aq {
	AQueue* first;
	AQueue* last;
} First_AQ;
typedef First_AQ* QueueA;

typedef struct bqueue{
	int maxsize;
	int first;
	int last;
	int n;
	int* array;
} BQueue;
typedef BQueue* QueueB;

QueueA InitQueueA() {
	QueueA Q = malloc(sizeof(First_AQ));
	if (Q) {
		Q->first = NULL;
		Q->last = NULL;
		return Q;
	}
	else {
		return NULL;
	}
}

QueueB InitQueueB(int size) {
	QueueB Q = malloc(sizeof(BQueue));
	if (Q) {
		Q->maxsize = size;
		Q->first = 0;
		Q->last = -1;
		Q->n = 0;
		Q->array = malloc(Q->maxsize * sizeof(int));
		return Q;
	}
	else {
		return NULL;
	}
}

int QueueEmptyA(QueueA Q) {
	return Q->first == NULL;
}

int QueueEmptyB(QueueB Q) {
	return Q->n == 0;
}

int QueueFullB(QueueB Q) {
	return Q->n == Q->maxsize;
}

int QueueFirstA(QueueA Q) {
	return Q->first->element;
}

int QueueFirstB(QueueB Q) {
	return Q->array[Q->first];
}

int QueueLastA(QueueA Q) {
	return Q->last->element;
}

int QueueLastB(QueueB Q) {
	return Q->array[Q->last];
}

void EnterQueueA(int x, QueueA Q) {
	AQueue* new_node = malloc(sizeof(AQueue));
	if (new_node) {
		new_node->element = x;
		new_node->next = NULL;
		if (QueueEmptyA(Q)) {
			Q->first = new_node;
			Q->last = new_node;
		}
		else {
			Q->last->next = new_node;
			Q->last = new_node;
		}
	}
}

void EnterQueueB(int x, QueueB Q) {
	if (!QueueFullB(Q)) {
		Q->last += 1;
		Q->last %= Q->maxsize;
		Q->array[Q->last] = x;
		Q->n += 1;
	}
}

int DeleteQueueA(QueueA Q) {
	if (!QueueEmptyA(Q)) {
		AQueue* prev_first = Q->first;
		Q->first = prev_first->next;
		int temp = prev_first->element;
		free(prev_first);
		return temp;
	}
	else {
		return 0;
	}
}

int DeleteQueueB(QueueB Q) {
	if (!QueueEmptyB(Q)) {
		int temp = Q->array[Q->first];
		Q->first += 1;
		Q->first %= Q->maxsize;
		Q->n -= 1;
		return temp;
	}
	else {
		return 0;
	}
}

void main_Queue() {
	QueueB Q = InitQueueB(3);
	EnterQueueB(2029, Q);
	EnterQueueB(12, Q);
	int result = DeleteQueueB(Q);
	EnterQueueB(24, Q);
	EnterQueueB(521, Q);
	EnterQueueB(13, Q);
	result = DeleteQueueB(Q);
	EnterQueueB(14, Q);
}