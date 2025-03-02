"""Using an object-oriented approach to create a neural
network that supports both fully-connected and convolutional
layers"""

import numpy as np
from scipy import signal
from typing import Optional, Type, Literal

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

class ConvLayer(Layer):
    """See YouTube video for full breakdown of principles behind why this works
    https://www.youtube.com/watch?v=Lakz2MoHy6o"""
    def __init__(self, input_shape: tuple[int, int, int],
                 kernel_size: int, num_kernels: int):
        (self.input_depth,
        input_height,
        input_width) = input_shape
        self.depth = num_kernels
        self.input_shape = input_shape
        self.output_shape = (self.depth, 
                             input_height - kernel_size + 1, 
                             input_width - kernel_size + 1)
        self.kernels_shape = (self.depth, self.input_depth, 
                              kernel_size, kernel_size)
        self.kernels = np.random.randn(*self.kernels_shape)
        self.biases = np.random.randn(*self.output_shape)
        print(self.output_shape)

    def forward(self, input_data):
        self.input_data = input_data
        self.output_data = np.copy(self.biases)
        for i in range(self.depth):
            for j in range(self.input_depth):
                print(f"{self.input_data[j][0].ndim}, {self.kernels[i, j].ndim}")
                self.output_data[i] += signal.correlate2d(self.input_data[j][0], self.kernels[i, j], 'valid')
                
        return self.output_data
    
    def backward(self, output_grad):
        self.bias_grad = output_grad.copy()
        self.kernels_gradient = np.zeros(self.kernels_shape)
        self.input_gradient = np.zeros(self.input_shape)

        for i in range(self.depth):
            for j in range(self.input_depth):
                self.kernels_gradient[i, j] = signal.correlate2d(self.input_data[j], output_grad[i], 'valid')
                self.input_gradient[j] += signal.convolve2d(output_grad[i], self.kernels[i, j], 'full')

    @property
    def get_params_and_grads(self):
        # Return parameters with their corresponding gradients
        return [(self.kernels, self.kernels_gradient), (self.biases, self.bias_grad)]


class ConvLayerHmm(Layer):
    def __init__(self, input_shape: tuple[int, int, int], 
                kernel_size: int, num_filters: int, 
                stride=1, padding=0):
        """
        Convolutional Layer
        
        Parameters:
        -----------
        input_shape : tuple
            Shape of input (channels, height, width)
        kernel_size : int
            Size of the convolutional kernel (square)
        num_filters : int
            Number of convolutional filters
        stride : int
            Stride of the convolution
        padding : int
            Zero padding to add to the input
        """
        self.input_shape = input_shape
        self.in_channels = input_shape[0]
        self.kernel_size = kernel_size
        self.num_filters = num_filters
        self.stride = stride
        self.padding = padding
        
        # Initialize weights and bias
        self.weights = np.random.randn(num_filters, self.in_channels, kernel_size, kernel_size) * 0.01
        self.bias = np.zeros((num_filters, 1))
        
        # Cache for backward pass
        self.input = None
        self.output = None
        
        # For use with optimizer
        self.weight_gradients = np.zeros_like(self.weights)
        self.bias_gradients = np.zeros_like(self.bias)
    
    def _pad_input(self, x):
        """Add zero padding to the input"""
        if self.padding > 0:
            return np.pad(
                x, 
                ((0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)), 
                'constant'
            )
        return x
    
    def forward(self, x):
        batch_size, _, height, width = x.shape
        self.input = x
        
        # Pad input
        x_padded = self._pad_input(x)
        
        # Calculate output dimensions
        out_height = (height + 2 * self.padding - self.kernel_size) // self.stride + 1
        out_width = (width + 2 * self.padding - self.kernel_size) // self.stride + 1
        
        # Initialize output
        output = np.zeros((batch_size, self.num_filters, out_height, out_width))
        
        # Implement convolution using tensordot for each spatial location
        for h in range(out_height):
            for w in range(out_width):
                h_start = h * self.stride
                h_end = h_start + self.kernel_size
                w_start = w * self.stride
                w_end = w_start + self.kernel_size
                
                # Extract patches [batch, channels, kernel_size, kernel_size]
                patches = x_padded[:, :, h_start:h_end, w_start:w_end]
                
                # Use tensordot to compute output for this position
                # Sum over channels and both spatial dimensions (axes 1, 2, 3)
                output[:, :, h, w] = np.tensordot(patches, self.weights, axes=([1, 2, 3], [1, 2, 3]))
        
        # Add bias to each filter's output
        for f in range(self.num_filters):
            output[:, f] += self.bias[f]
        
        self.output = output
        return output

    def backward(self, grad_output: np.ndarray):
        # Initialize gradients
        grad_input = np.zeros_like(self.input)
        self.weight_gradients = np.zeros_like(self.weights)
        self.bias_gradients = np.sum(grad_output, axis=(0, 2, 3))  # Sum over batch, height, width

        # Pad input and gradient input
        input_padded = self._pad_input(self.input)
        grad_input_padded = np.pad(grad_input, ((0, 0), (0, 0), (self.padding, self.padding), (self.padding, self.padding)))

        # Extract patches using strided slicing
        patches = np.lib.stride_tricks.sliding_window_view(
            input_padded, (self.kernel_size, self.kernel_size), axis=(2, 3)
        )[:, :, ::self.stride, ::self.stride]

        # Compute weight gradients using tensordot
        self.weight_gradients = np.tensordot(grad_output, patches, axes=([0, 2, 3], [0, 2, 3]))

        # Compute input gradients using tensordot
        flipped_weights = np.flip(self.weights, axis=(2, 3))  # Flip spatial dimensions
        grad_input_padded = np.tensordot(grad_output, flipped_weights, axes=([1], [0]))

        # Remove padding if applied
        if self.padding > 0:
            grad_input = grad_input_padded[:, :, self.padding:-self.padding, self.padding:-self.padding]
        else:
            grad_input = grad_input_padded

        return grad_input
    
    @property
    def get_params_and_grads(self):
        """Get parameters and gradients for optimizer"""
        return [(self.weights, self.weight_gradients), (self.bias, self.bias_gradients)]
    
class FlattenLayer:
    def __init__(self):
        """
        Flatten layer to transition from convolutional layers to fully connected layers
        """
        self.input_shape = None
    
    def forward(self, x):
        """
        Forward pass - flatten input from (batch_size, channels, height, width) to (batch_size, channels*height*width)
        """
        self.input_shape = x.shape
        batch_size = x.shape[0]
        return x.reshape(batch_size, -1)
    
    def backward(self, grad_output):
        """
        Backward pass - reshape gradient back to the original input shape
        """
        return grad_output.reshape(self.input_shape)
    
    @property
    def get_params_and_grads(self):
        """No parameters to update"""
        return None
    
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
        # Compute gradient using element-wise multiplication (efficient)
        softmax_grad = self.output * (grad_output - np.sum(grad_output * self.output, axis=1, keepdims=True))
        
        return softmax_grad

### Loss functions ###

class LossFunction:
    def __init__(self, reg_method: Literal['l1','l2'], lambda_regularisation: float=0):
        self.lambda_ = lambda_regularisation
        self.regularisation = reg_method
    
    def forward(self, predicted:np.ndarray, target: np.ndarray, model: Type['NeuralNetwork']):
        raise NotImplementedError
    
    def backward(self):
        raise NotImplementedError
    
    def __str__(self):
        return f'{type(self).__name__}'

class MSELoss(LossFunction):
    def __init__(self, reg_method, lambda_regularisation = 0):
        super().__init__(reg_method, lambda_regularisation)

    def forward(self, predicted: np.ndarray, target: np.ndarray, model:Type['NeuralNetwork']):
        # Store for backward pass
        self.predicted = predicted
        self.target = target
        # Compute mean squared error
        loss = np.mean((predicted - target) ** 2)

        # Add L1/2 regularization term (if model is provided)
        if model:
            # Sum of squared weights for L2 regularization
            reg = 0
            for layer in model.layers:
                if hasattr(layer, 'weights'):
                    match self.regularisation:
                        case 'l1':
                            reg += np.sum(np.abs(layer.weights))
                        case 'l2':
                            reg += np.sum(layer.weights ** 2)


            loss += self.lambda_ * reg

        return loss

    def backward(self):
        gradient = 2* (self.predicted - self.target) / self.predicted.size
        return gradient

class CrossEntropyLoss(LossFunction):
    def __init__(self, reg_method: Literal['l1', 'l2'] = None, lambda_regularisation: float = 0):
        super().__init__(reg_method, lambda_regularisation)
        self.predicted = None  # Store predicted values for backward pass
        self.target = None      # Store target values for backward pass

    def forward(self, predicted: np.ndarray, target: np.ndarray, model: Type['NeuralNetwork']):
        batch_size = predicted.shape[0]
        
        # Stabilize predictions to prevent log(0)
        predicted = np.clip(predicted, 1e-15, 1 - 1e-15)

        # Compute cross-entropy loss
        loss = -np.sum(target * np.log(predicted)) / batch_size

        # Store for backward pass
        self.predicted = predicted
        self.target = target

        # Apply regularization
        if self.lambda_ > 0:
            if self.regularisation == "l1":
                reg_loss = self.lambda_ * sum(np.sum(np.abs(layer.weights)) for layer in model.layers if hasattr(layer, 'weights'))
            elif self.regularisation == "l2":
                reg_loss = self.lambda_ * sum(np.sum(layer.weights ** 2) for layer in model.layers if hasattr(layer, 'weights'))
            else:
                reg_loss = 0
            loss += reg_loss / batch_size  # Normalize by batch size

        return loss

    def backward(self):
        """
        Compute the gradient of the cross-entropy loss with respect to predictions.

        Returns:
        --------
        np.ndarray
            The computed gradient with shape (batch_size, num_classes).
        """
        batch_size = self.predicted.shape[0]
        return (self.predicted - self.target) / batch_size  # Normalized gradient

    def __str__(self):
        return f'CrossEntropyLoss (Regularization: {self.regularisation}, λ: {self.lambda_})'
        

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
            param -= self.learning_rate * grad.reshape(param.shape)
        
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
                total_loss += loss.forward(predictions, y_batch, self)
                
                # Backward pass
                grad_loss = loss.backward()
                self.backward(grad_loss)
                
                # Update parameters using the optimiser            
                optimiser.step(self.get_params_and_grads)

            self.losses.append(total_loss)

            if epoch % 10 == 9:
                print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss:.4f}")

    def predict(self, X_test: np.ndarray):
        """
        Make predictions on test data
        """
        return self.forward(X_test)
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray):
        """
        Evaluate the model on test data and return the loss
        """
        predictions = self.predict(X_test)
        test_loss = self.loss.forward(predictions, y_test, self)
        return test_loss, predictions
