#include <stdio.h>
#include <stdlib.h>

typedef struct astack {
	int top;
	int maxtop;
	int* data;
} Astack;
typedef struct astack* StackA;

StackA InitStack(int size) {
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

int StackEmpty(StackA S) {
	return S->top < 0;
}

int StackFull(StackA S){
	return S->top >= S->maxtop - 1;
}

int StackTop(StackA S) {
	if (StackEmpty(S)) {
		return 0;
	}
	else {
		return S->data[S->top];
	}
}

void Push(int x, StackA S) {
	if (!StackFull(S)) {
		S->top += 1;
		S->data[S->top] = x;
	}
}

int Pop(StackA S) {
	if (StackEmpty(S)) {
		return 0;
	}
	else {
		int temp = S->data[S->top];
		//free(S->data[S->top]);
		S->top -= 1;
		return temp;
	}

}

void main_Stack() {
	StackA S = InitStack(6);
	int result = StackEmpty(S);
	Push(2016, S);
	Push(7, S);
	Push(12, S);
	result = Pop(S);
	result = Pop(S);
	result = Pop(S);
	Push(2029, S);
	Push(12, S);
	Push(24, S);
	Push(14, S);
	Push(13, S);
	Push(520, S);
}