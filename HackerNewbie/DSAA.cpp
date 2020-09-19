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
	neuron n = neuron(2);
	n.set_bias(1.0);
	double weights[2] = { 0.5,0.25 };
	n.set_weights(weights, 2);
	double inputs[3] = { 2,4,3 };
	double result = n.output_value(inputs, 3);
	printf("%f", result);
}