#include <iostream>
#include <vector>

using namespace std;

class neuron {
public:
	int input_dim;
	vector<double> weights;
	double bias;
	string activation;
	neuron(int dim) {
		this->input_dim = dim;
		this->activation = "sigmoid";
		for (int i = 0; i < this->input_dim; i++) {
			this->weights.push_back(1.0);
		}
		this->bias = 0;
	};
	void set_bias(double input_bias) {
		this->bias = input_bias;
	};
	void set_weights(double input_weights[], int size) {
		for (int i = 0; i < size; i++) {
			this->weights[i] = input_weights[i];
		}
	};
	double output_value(double input_values[], int size) {
		int length;
		if (size < this->input_dim) {
			length = size;
		}
		else {
			length = this->input_dim;
		}
		double output_temp = 0;
		for (int i = 0; i < length; i++) {
			input_values[i] *= this->weights[i];
			output_temp += input_values[i];
		}
		output_temp += this->bias;
		return activate(output_temp);
	};
	double activate(double before_activation) {
		if (this->activation.compare("sigmoid") == 0) {
			return 1 / (1 + exp(-before_activation));
		}
		else {
			return before_activation;
		}
	};
};


class layer {
public:
	int input_dim;
	int output_dim;
	vector<neuron> neurons;
	layer(int i_d, int o_d) {
		this->input_dim = i_d;
		this->output_dim = o_d;
		for (int i = 0; i < this->output_dim; i++) {
			neuron temp_n = neuron(this->input_dim);
			this->neurons.push_back(temp_n);
		}
	};
	vector<double> forward(double input_values[],int size) {
		vector<double> output_values;
		for (int i = 0; i < this->output_dim; i++) {
			double result = this->neurons[i].output_value(input_values, size);
			output_values.push_back(result);
		}
		return output_values;
	};
};