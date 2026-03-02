#include <iostream>

using namespace std;

void sphere_surface() {
	double radius;
	cout << "Input radius:\n";
	cin >> radius;
	double result = radius * radius * 3.14 * 4;
	cout << "Result is: " << result << "\n";
}