import numpy as np
import random
np.set_printoptions(suppress=True)

class Dense_layer():
    def __init__(self, input_size, output_size, activation="sigmoid", weights=None, biases=None):
        
        if np.any(weights) == None:
            self.weights = np.random.randn(input_size, output_size)
        else:
            self.weights = self.mutate(weights)

        if np.any(biases) == None:
            self.biases = np.zeros((1, output_size))
        else:
            self.biases = self.mutate(biases)

        self.activation = activation

    def forward(self, input):
        self.input = input
        self.output = np.dot(input, self.weights) + self.biases

        if self.activation == "sigmoid":
            return self.sigmoid(self.output)
        elif self.activation == "relu":
            return self.relu(self.output)
        elif self.activation == "softmax":
            return self.softmax(self.output)

    def sigmoid(self, x):
        self.sigmoid_func = 1.0 / (1.0 + np.exp(-x))
        return self.sigmoid_func

    def d_sigmoid(self, x):
        self.d_sigmoid_func = np.multiply(x, 1.0-x)
        return self.d_sigmoid_func
    
    def relu(self, x):
        self.relu_func = np.maximum(x, 0)
        return self.relu_func

    def d_relu(self, x):
        return x > 0
    
    def softmax(self, x):
        self.exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        self.softmax_func = self.exps / np.sum(self.exps, axis=1, keepdims=True)
        return self.softmax_func
    
    def d_softmax(self, x):
        return x * (1 - x)
    
    def mutate(self, x):
        m, n = x.shape
        return np.multiply(x, np.random.uniform(low=0.90, high=1.1, size=(m, n)))


class Network:
    def __init__(self, setup=None):
        if setup == None:
            self.setup = [
                Dense_layer(2, 16),
                Dense_layer(16, 1),
            ]
        else:
            self.setup = []
            for layer in setup:
                m, n = layer.shape
                self.setup.append(Dense_layer(m, n, weights=layer))



    def predict(self, X):
        output = X
        for layer in self.setup:
            output = layer.forward(output)

        return output