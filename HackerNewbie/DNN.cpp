#include <iostream>
#include <vector>
#include <DNN.h>

using namespace std;

class neuron {
	int input_dim;
	vector<double> weights;
	double bias;
	string activation;
public:
	neuron(int dim) {
		this->input_dim = dim;
		this->activation = "sigmoid";
		for (int i = 0; i < this->input_dim; i++) {
			this->weights.push_back(1.0);
		}
		this->bias = 0;
	}
	void set_bias(double input_bias) {
		this->bias = input_bias;
	}
	void set_weights(double input_weights[], int size) {
		for (int i = 0; i < size; i++) {
			this->weights[i] = input_weights[i];
		}
	}
	double output_value(double input_values[], int size) {
		int length;
		bool padding;
		if (size < this->input_dim) {
			length = size;
			padding = true;
		}
		else {
			length = this->input_dim;
			padding = false;
		}
		double output_temp = 0;
		for (int i = 0; i < length; i++) {
			input_values[i] *= this->weights[i];
			output_temp += input_values[i];
		}
		output_temp += this->bias;
		return activate(output_temp);
	}
	double activate(double before_activation) {
		if (this->activation.compare("sigmoid")) {
			return 1 / (1 + exp(-before_activation));
		}
		else {
			return before_activation;
		}
	}
};