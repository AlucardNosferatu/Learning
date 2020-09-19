#include <iostream>
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
	neuron n = new neuron(2);

}