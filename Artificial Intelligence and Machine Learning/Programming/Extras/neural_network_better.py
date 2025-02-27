"""Using an object-oriented approach to create a neural
network that supports both fully-connected and convolutional
layers"""

import numpy as np
import pandas as pd
from typing import Optional

### Layer types ###

class Layer:
    def forward(self, input_data: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    
    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    
    @property
    def get_params_and_grads(self):
        raise NotImplementedError

class FullyConnected(Layer):
    def __init__(self, input_dim, output_dim):
        self.weights = np.random.randn(input_dim, output_dim) * np.sqrt(2 / input_dim)
        self.bias = np.zeros((1, output_dim))
    
    def forward(self, input_data) -> np.ndarray:
        self.input = input_data  # Cache for backpropagation
        return np.dot(input_data, self.weights) + self.bias
    
    def backward(self, grad_output) -> np.ndarray:
        # Compute gradients
        self.grad_weights = np.dot(self.input.T, grad_output)
        self.grad_bias = np.sum(grad_output, axis=0, keepdims=True)
        # Return gradient with respect to the input data for backpropagation
        return np.dot(grad_output, self.weights.T)
    
    @property
    def get_params_and_grads(self):
        # Return parameters with their corresponding gradients
        return [(self.weights, self.grad_weights), (self.bias, self.grad_bias)]
    
### Activation Layers ###

class ActivationLayer(Layer):
    def forward(self, input_data):
        return super().forward(input_data)
    
    def backward(self, grad_output):
        return super().backward(grad_output)
    
    @property
    def get_params_and_grads(self):
        return None

class Sigmoid(ActivationLayer):
    def forward(self, input_data):
        self.output = 1 / (1 + np.exp(-input_data))
        return self.output

    def backward(self, grad_output):
        return grad_output * self.output * (1 - self.output)
    
class ReLU(ActivationLayer):
    def forward(self, input_data):
        self.input = input_data
        return np.maximum(0, input_data)
    
    def backward(self, grad_output):
        grad_output[self.input <= 0] = 0
        return grad_output

class Softmax(ActivationLayer):
    """Not ideal to implement if not used in conjunction with cross-entropy"""
    def forward(self, input_data):
        stable_exp = np.exp(input_data - np.max(input_data, axis=-1, keepdims=True))
        self.output = stable_exp / np.sum(stable_exp, axis=-1, keepdims=True)
        return self.output

    def backward(self, grad_output):
        s = self.output.reshape(-1, 1)
        return np.diagflat(s) - np.dot(s, s.T)  # Not great as it runs in O(n^2) time

### Loss functions ###

class MSELoss:
    def forward(self, predicted: np.ndarray, target: np.ndarray):
        # Store for backward pass
        self.predicted = predicted
        self.target = target
        # Compute mean squared error
        loss = np.mean((predicted - target) ** 2)
        return loss

    def backward(self):
        gradient = 2* (self.predicted - self.target) / self.predicted.size
        return gradient
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f'{type(self).__name__}'

### Optimisers ###

class Optimiser:
    def __init__(self, learning_rate=0.01, batch_size: Optional[int]=None):
        self.learning_rate = learning_rate
        self.batch_size = batch_size

    def get_batches(self):
        raise NotImplementedError

    def step(self, parameters):
        raise NotImplementedError
    
    def zero_grad(self):
        """Used for momentum-based optimisers like Adam, RMSprop and SGD with momentum"""
        raise NotImplementedError
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f'{type(self).__name__}, Learning rate: {self.learning_rate}, Batch size: {self.batch_size}'

class SGD(Optimiser):
    def __init__(self, learning_rate=0.01, batch_size: Optional[int]=None):
        self.learning_rate = learning_rate
        self.batch_size = batch_size

    def get_batches(self, X_train: np.ndarray, y_train: np.ndarray):
        """Yield mini-batches (or full-batch if batch_size=None)."""
        num_samples = X_train.shape[0]
        indices = np.random.permutation(num_samples)

        if self.batch_size and self.batch_size >= num_samples:
            self.batch_size = None

        if self.batch_size is None:
            # Standard gradient descent, no batches
            yield X_train, y_train
        else:
            # Batches
            for i in range(0, num_samples, self.batch_size):
                batch_indices = indices[i:i + self.batch_size]
                yield X_train[batch_indices], y_train[batch_indices]
    
    def step(self, parameters):
        for param, grad in parameters:
            param -= self.learning_rate * grad
        
        self.zero_grad()
    
    def zero_grad(self):
        pass

### Neural Network ###

class NeuralNetwork:
    def __init__(self):
        self.layers: list[Layer] = []
    
    def add(self, layer: Layer):
        self.layers.append(layer)
    
    def forward(self, x: np.ndarray):
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def backward(self, grad: np.ndarray):
        # Propagate gradients backwards through each layer in reverse order
        # Requires loss function to calculate loss
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
        return grad
    
    @property
    def get_params_and_grads(self):
        params_and_grads = []
        for layer in self.layers:
            if layer.get_params_and_grads is not None:
                params_and_grads.extend(layer.get_params_and_grads)
        return params_and_grads
    
    def fit(self, X_train: np.ndarray, y_train: np.ndarray, 
            loss, optimiser: Optimiser, num_epochs: int=500):
        # I'd like to put the training method in here, but I think that might require
        # integrating loss functions into the network itself.
        # It can be done!
        
        # Required to fix broadcasting issues that otherwise prevented networks
        # from having flexible structures - much faster now!
        y_train = y_train.reshape(-1, 1)

        # Losses held in a list so I can output how the 
        # loss changes over the course of training
        self.losses = []

        self.optimiser = optimiser
        self.loss = loss
        self.num_epochs = num_epochs

        print(f'''Training with the following parameters:
    Loss Function: {loss}
    Optimiser: {optimiser}
    Epochs: {num_epochs}''')
        for epoch in range(num_epochs):
            total_loss = 0

            for X_batch, y_batch in optimiser.get_batches(X_train, y_train):
                # Forward pass
                predictions = self.forward(X_batch)
                total_loss += loss.forward(predictions, y_batch)
                
                # Backward pass
                grad_loss = loss.backward()
                self.backward(grad_loss)
                
                # Update parameters using the optimiser            
                optimiser.step(self.get_params_and_grads)

            self.losses.append(total_loss)
            print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss:.4f}")
        

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load data
diabetes = load_diabetes()
X, y = diabetes.data, diabetes.target

# Preprocess the data (e.g., scaling)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

network = NeuralNetwork()

""" network.add(FullyConnected(X_train.shape[1], 128))
network.add(FullyConnected(128, 64)) """

# Network architecture
network.add(FullyConnected(X_train.shape[1], 256))
network.add(ReLU())
network.add(FullyConnected(256, 128))
network.add(ReLU())
network.add(FullyConnected(128, 64))
network.add(ReLU())
network.add(FullyConnected(64, 10))

network.fit(X_train, y_train, MSELoss(), SGD(learning_rate=.00001, batch_size=128), num_epochs=2000)

from matplotlib import pyplot as plt
fig, ax = plt.subplots()

ax.plot(pd.Series(network.losses))
ax.set_ylabel('Loss')
ax.set_xlabel('Epoch')
ax.set_title(f'{network.loss}, {network.optimiser},\n{network.num_epochs} epochs')

plt.show()
