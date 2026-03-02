#include <iostream>
#include "DNN.cpp"

using namespace std;

extern void Iamastudent();
extern void star_tower(int max, int now);
extern void sphere_surface();

int a = 0;

int func1() {
	a = 2;
	return 2;
}

int func2() {
	a = 3;
	return 3;
}

int func3() {
	a = 4;
	return 4;
}

int main() {
	layer l = layer(2, 3);
	double input_values[2] = { 3.0,4.0 };
	vector<double> result = l.forward(input_values, 2);
	for (int i = 0; i < 3; i++) {
		printf("%f ", result[i]);
	}
}