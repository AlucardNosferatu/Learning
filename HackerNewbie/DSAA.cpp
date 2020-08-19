#include <iostream>

using namespace std;

extern void Iamastudent();
extern void star_tower(int max, int now);
extern void sphere_surface();


int main() {
	//sphere_surface();
	char i[3] = {"ab"};
	char* ip=i;
	cout << *ip << "\n";
	ip += 1;
	cout << *ip << "\n";
}