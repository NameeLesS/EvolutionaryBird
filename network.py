import numpy as np

class Network:
    def __init__(self, input_size, n_neurons=10):
        self.input_size = input_size
        self.n_neurons = n_neurons
        self.fcl_1 = FullyConnectedLayer(input_size=input_size, n_neurons=n_neurons)
        self.output = FullyConnectedLayer(input_size=n_neurons, n_neurons=1)
        

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

    def get_weights(self):
        return np.array([self.fcl_1.weights.flatten(), self.output.weights.flatten(), self.fcl_1.biases.flatten(), self.output.biases.flatten()])
        
    
    def load_weights(self, weights):
        end_idx = self.input_size * self.n_neurons
        self.fcl_1.weights = weights[: end_idx].reshape((self.input_size, self.n_neurons))
        self.output.weights = weights[end_idx: end_idx + self.n_neurons]

        end_idx += self.n_neurons
        self.fcl_1.biases = weights[end_idx: end_idx + self.n_neurons]

        end_idx += self.n_neurons
        self.output.biases = weights[end_idx: end_idx + 1]



class FullyConnectedLayer:
    def __init__(self, input_size, n_neurons):
        self.weights = np.random.randn(input_size * n_neurons).reshape((input_size, n_neurons))
        self.biases = np.random.randn(n_neurons)
    
    def __call__(self, x):
        return np.matmul(x, self.weights) + self.biases # TODO: Check if it is correctly implemented
    

# network = Network(2)
# print(network.predict(np.array([2, 3]).reshape(1, -1)))