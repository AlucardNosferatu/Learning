#include <stdio.h>
#include <stdlib.h>

int findMax(int int_list[], int length) {
	int a = 0;
	int b = 0;
	if (length == 1) {
		return int_list[0];
	}
	else if (length >= 2) {
		int a_length = length / 2;
		int b_length = length - a_length;
		a = findMax(int_list, a_length);
		b = findMax(int_list + a_length, b_length);
	}
	else {
		printf("You fucked up!");
	}
	if (a > b) {
		return a;
	}
	else {
		return b;
	}

}


void main_DAC() {
	int test_list[11] = { 85,23,435,213,23,141,51,34,123,123,351 };
	int result = findMax(test_list, 11);
}