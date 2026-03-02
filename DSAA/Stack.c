#include <stdio.h>
#include <stdlib.h>

typedef struct astack {
	int top;
	int maxtop;
	int* data;
} Astack;
typedef struct astack* StackA;

typedef struct bstack {
	int element;
	struct bstack* next;
} Bstack;
typedef struct bs_first {
	Bstack* next;
} Bstack_f;
typedef struct bs_first* StackB;


StackA InitStackA(int size) {
	StackA S = malloc(sizeof(Astack));
	if (S) {
		S->maxtop = size;
		S->top = -1;
		S->data = malloc(S->maxtop * sizeof(int));
		return S;
	}
	else {
		return NULL;
	}
}

StackB InitStackB() {
	StackB S = malloc(sizeof(StackB));
	if (S) {
		S->next = NULL;
		return S;
	}
	else {
		return NULL;
	}
}

int StackEmptyA(StackA S) {
	return S->top < 0;
}

int StackEmptyB(StackB S) {
	return S->next == NULL;
}

int StackFullA(StackA S){
	return S->top >= S->maxtop - 1;
}

int StackFullB() {
	Bstack* S_p;
	S_p = malloc(sizeof(Bstack));
	if (S_p) {
		free(S_p);
		return 0;
	}
	else {
		return 1;
	}
}

int StackTopA(StackA S) {
	if (StackEmptyA(S)) {
		return 0;
	}
	else {
		return S->data[S->top];
	}
}

int StackTopB(StackB S) {
	if (!StackEmptyB(S)) {
		return S->next->element;
	}
	else {
		return 0;
	}
}

void PushA(int x, StackA S) {
	if (!StackFullA(S)) {
		S->top += 1;
		S->data[S->top] = x;
	}
}

void PushB(int x, StackB S) {
	if (!StackFullB()) {
		Bstack* prev_first = S->next;
		Bstack* new_first = malloc(sizeof(Bstack));
		if (new_first) {
			new_first->element = x;
			new_first->next = prev_first;
			S->next = new_first;
		}
	}
}

int PopA(StackA S) {
	if (StackEmptyA(S)) {
		return 0;
	}
	else {
		int temp = S->data[S->top];
		//free(S->data[S->top]);
		S->top -= 1;
		return temp;
	}

}

int PopB(StackB S) {
	if (!StackEmptyB(S)) {
		Bstack* prev_first = S->next;
		S->next = S->next->next;
		int temp = prev_first->element;
		free(prev_first);
		return temp;
	}
	else {
		return 0;
	}
}

void main_Stack() {

}