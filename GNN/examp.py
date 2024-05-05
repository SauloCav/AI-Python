import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class GraphConvolution(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(GraphConvolution, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x, adj):
        x = torch.matmul(adj, x)  # Matrix multiplication by adjacency matrix
        x = self.linear(x)
        return F.relu(x)

class GraphNeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GraphNeuralNetwork, self).__init__()
        self.gc1 = GraphConvolution(input_dim, hidden_dim)
        self.gc2 = GraphConvolution(hidden_dim, output_dim)

    def forward(self, x, adj):
        x = self.gc1(x, adj)
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)

# Example graph data (adjacency matrix and node features)
adjacency_matrix = torch.tensor([[0, 1, 0, 0],
                                 [1, 0, 1, 0],
                                 [0, 1, 0, 1],
                                 [0, 0, 1, 0]], dtype=torch.float32)

node_features = torch.tensor([[0.1, 0.2],
                               [0.3, 0.4],
                               [0.5, 0.6],
                               [0.7, 0.8]], dtype=torch.float32)

# Define model
input_dim = node_features.shape[1]
hidden_dim = 16
output_dim = 2  # Number of classes
model = GraphNeuralNetwork(input_dim, hidden_dim, output_dim)

# Forward pass
output = model(node_features, adjacency_matrix)
print("Output probabilities:\n", torch.exp(output))
