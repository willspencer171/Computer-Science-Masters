"""Nice and simple neural network that implements layers one by one as functions
the network itself is a function too"""
import numpy as np

def linear(x, W, b):
    """Linear transformation."""
    return np.dot(W, x) + b

def relu(x):
    """ReLU activation function."""
    return np.maximum(0, x)

def softmax(x):
    """Softmax activation function."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def neural_network(x, weights, biases, activations):
    for i in range(len(weights)):
        x = activations[i](np.dot(weights[i], x) + biases[i])
    return x

def apply_layer(x, W, b, activation):
    """Apply a single layer: linear transformation followed by an activation."""
    return activation(linear(x, W, b))

def forward_feed_nn(x, layers, params):
    """
    Recursively applies layers to input x.
    
    Parameters
    ---
        x
            the input vector.
        layers
            a list of activation functions for each layer.
        params
            a list of tuples (W, b) for each layer.

    Returns
    ---
        The output after applying all layers. This represents the
        probability of an instance belonging to a specific class
    """
    for i in range(len(layers)):
        W, b = params[i]
        x = apply_layer(x, W, b, layers[i])  # Apply layer and update x
    return x

layers = [relu, lambda x: x, lambda x: x]

params = [
    (np.random.randn(4, 3), np.random.randn(4, 1)),
    (np.random.randn(2, 4), np.random.randn(2, 1)),
    (np.random.randn(3, 2), np.random.randn(3, 1))
]

x = np.random.randn(3, 1)

output = forward_feed_nn(x, layers, params)
print(output)
