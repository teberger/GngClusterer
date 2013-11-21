import networkx as nx
import random
from functools import partial

class gng(networkx):
    def __init__(self, error_fn, node_gen, learning_rate):
        self.node_generator = node_gen
        self.err_fn = error_fn
        self.learning_rate = learning_rate

        #initialize the network to two points
        rand_point_x = node_gen.generate(mode = "random")
        rand_point_x = node_gen.generate(mode = "random")
        self.network = nx.Graph()
        self.network.add_node(rand_point_x)
        self.network.add_node(rand_point_y)
        self.network.add_edge(rand_point_x, rand_point_y)

    def grow(self):
        #find node with highest error -- distance to closest node
        err_node = self.error_fn(self.network.nodes(), mode="max")

        #find connected node with highest error
        err_neighbor = self.error_fn(self.network.edge(err_node), mode="max")

        #delete edge between the two
        self.network.remove_edge(err_node, err_neighbor)

        #insert new node
        new_node = self.node_generator.generate(mode = "average", x = err_node, y = err_neighbor)

        #connect to other two nodes with highest error
        self.network.add_edge(err_node, new_node)
        self.network.add_edge(err_neighbor, new_node)

    def fit(self, point):
        #search for nearest neighbors        
        #dynamic neighborhood size of 5% of the network
        neighborhood_size = int(self.network.node() * 0.05)

        #stimulate graph using underlying data -- point param
        best_nodes = self.error_fn(self.network.nodes(), mode="min", size = neighborhood_size)

        #pull nodes in direction of stimulation
        diminishing_return = 0.9
        alpha = self.learning_rate
        for node in best_nodes:
            new_node = self.node_generator.generate(mode = "average", x = node, y = point, x_weight = 1-alpha, y_weight = alpha)
            alpha = alpha * diminishing_return
            self.network[node] = new_node
