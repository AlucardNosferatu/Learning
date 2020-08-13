#include <stdio.h>
#include <stdlib.h>
#include "LinkTable.c"

extern int LinkLength(NodeP NP, int count);

int GetNode(NodeFP NFP,int index) {
	NodeP NP = NFP->next;
	if (NP) {
		for (int i = 0; i < index; i++) {
			NP = NP->next;
		}
		return NP->value;
	}
	else {
		return 0;
	}
}

void Pop(NodeFP NFP) {
	NodeP NP = NFP->next;
	NodeP deleted = NP;
	if (NP->next) {
		while (NP->next->next) {
			NP = NP->next;
		}
		deleted = NP->next;
		NP->next = NULL;
	}
	else {
		NFP->next = NULL;
	}
	free(deleted);
}

void Append(NodeFP NFP, int x) {
	NodeP NP = NFP->next;
	if (NP) {
		while (NP->next) {
			NP = NP->next;
		}
		NP->next = malloc(sizeof(Node));
		if (NP->next) {
			NP->next->value = x;
			NP->next->next = NULL;
			NP->next->prev = NULL;
		}
	}
	else {
		NFP->next = malloc(sizeof(Node));
		if (NFP->next) {
			NFP->next->value = x;
			NFP->next->next = NULL;
			NFP->next->prev = NULL;
		}
	}
}

void PrintLink(NodeFP NFP) {
	NodeP NP = NFP->next;
	if (NP) {
		if (NP->value) {
			printf(" %d", NP->value);
		}
		if (NP->next) {
			PrintLink(NP->next);
		}
		else {
			printf("\n");
		}
	}
	else {
		printf("\n");
	}
}

void recursive(int n, NodeF lp_val_f) {
	NodeFP list_prev = &lp_val_f;
	NodeP list_content = list_prev->next;
	int length = LinkLength(list_content, 0);
	int last_value = GetNode(list_prev, length - 1);
	int switch_append = (length != 0);
	switch_append = switch_append && (last_value >= n);
	switch_append = switch_append || (length == 0);
	switch_append = switch_append || (n == 1);
	if (switch_append) {
		Append(list_prev, n);
		PrintLink(list_prev);
		if (n != 1) {
			Pop(list_prev);
		}
	}
	for (int i = 1; i < n; i++) {
		int temp = n - i;
		list_content = list_prev->next;
		int len = LinkLength(list_content, 0);
		int last_val = GetNode(list_prev, len - 1);
		int switch_recurse = (len == 0);
		switch_recurse = switch_recurse || (last_val >= temp);
		if (switch_recurse) {
			Append(list_prev, temp);
			recursive(i, *list_prev);
			Pop(list_prev);
		}
	}
}

void main_Decompose() {
	NodeFP NFP = malloc(sizeof(NodeF));
	if (NFP) {
		NFP->next = NULL;
		recursive(6, *NFP);
	}
}
