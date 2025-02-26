"""Using an object-oriented approach to create a neural
network that supports both fully-connected and convolutional
layers"""

import numpy as np

class Layer:
    def forward(self, input_data):
        raise NotImplementedError
    
    def backward_prop(self, grad_output):
        raise NotImplementedError

class FullyConnected(Layer):
    def __init__(self, input_dim, output_dim):
        self.weights = np.random.randn(input_dim, output_dim) * 0.01
        self.bias = np.zeros((1, output_dim))
    
    def forward(self, input_data):
        self.input = input_data  # Cache for backpropagation
        return np.dot(input_data, self.weights) + self.bias
    
    def backward(self, grad_output):
        # Compute gradients
        self.grad_weights = np.dot(self.input.T, grad_output)
        self.grad_bias = np.sum(grad_output, axis=0, keepdims=True)
        # Return gradient with respect to the input data for backpropagation
        return np.dot(grad_output, self.weights.T)

class NeuralNetwork:
    def __init__(self):
        self.layers = []
    
    def add(self, layer):
        self.layers.append(layer)
    
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def backward(self, grad):
        # Propagate gradients backwards through each layer in reverse order
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
        return grad
