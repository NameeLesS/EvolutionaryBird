import numpy as np

class Network:
    def __init__(self, input_size):
        self._weights = np.array([])

        self.fcl_1 = FullyConnectedLayer(input_size=input_size, n_neurons=10)
        self.output = FullyConnectedLayer(input_size=10, n_neurons=1)
        

    def predict(self, x):
        x = self.fcl_1(x)
        x = self._leaky_relu(x, 0.01)
        x = self.output(x)
        x = self._sigmoid(x)
        return x

    def _sigmoid(self, x):
        return 1 / (1 +  np.exp(-x))
    
    def _leaky_relu(self, x, a):
        return np.maximum(-a*x, x)

    @property
    def weights(self):
        return self._weights
    
    @weights.setter
    def weights(self, weights):
        self._weights = weights

    @weights.getter
    def weights(self):
        return self._weights


class FullyConnectedLayer:
    def __init__(self, input_size, n_neurons):
        self.weights = np.random.rand(input_size, n_neurons)
        self.biases = np.random.rand(n_neurons)
    
    def __call__(self, x):
        return np.matmul(x, self.weights) + self.biases # TODO: Check if it is correctly implemented
    

network = Network(2)
print(network.predict(np.array([2, 3]).reshape(1, -11)))