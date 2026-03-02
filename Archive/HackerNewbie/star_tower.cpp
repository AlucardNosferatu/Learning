#include <iostream>

void star_tower(int max,int now) {
	int lb = (max - now) / 2;
	int ub = lb + now;
	lb--;
	for (int i = 0; i < max; i++) {
		if ((i > lb) && (i < ub)) {
			std::cout << "*";
		}
		else {
			std::cout << " ";
		}
	}
	std::cout << "\n";
	if (now < max) {
		star_tower(max, now + 2);
		for (int i = 0; i < max; i++) {
			if ((i > lb) && (i < ub)) {
				std::cout << "*";
			}
			else {
				std::cout << " ";
			}
		}
		std::cout << "\n";
	}
}