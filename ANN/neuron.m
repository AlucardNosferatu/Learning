function output=neuron(input,link,bias)
z=dot(input,link)+bias;
output=1./(1.+exp(-z));
