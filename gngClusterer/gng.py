import networkx as nx
import random

class gng(object):
    def __init__(self, error_fn, node_gen, learning_rate, age_max):
        self.node_generator = node_gen
        self.err_fn = error_fn
        self.learning_rate = learning_rate
        self.age_max = age_max

        #initialize the network to two points
        rand_point_x = node_gen(mode = "random")
        rand_point_y = node_gen(mode = "random")
        self.network = nx.Graph()
        self.network.add_node(rand_point_x)
        self.network.add_node(rand_point_y)
        self.network.add_edge(rand_point_x, rand_point_y)
        self.network[rand_point_x][rand_point_y]['age'] = 0

    def grow(self):
        #find node with highest error -- distance to closest node
        (err_node, err) = self.error_fn(self.network.nodes(), mode="max")

        #find connected node with highest error
        (err_neighbor, err_n) = self.error_fn(self.network.neighbors(err_node), mode="max")

        #delete edge between the two
        self.network.remove_edge(err_node, err_neighbor)

        #insert new node
        new_node = self.node_generator(mode = "average", x = err_node, y = err_neighbor)
        #update local error of the largest nodes
        self.network[err_node]['error'] = self.network[err_node] * (1-self.learning_rate)
        self.network[err_neighbor]['error'] = self.network[err_neighbor] * (1-self.learning_rate)

        #connect to other two nodes with highest error
        self.network.add_node(new_node, error = (err + err_n)/2.0)
        self.network.add_edge(err_node, new_node)
        self.network[err_node][new_node]['age'] = 0
        self.network.add_edge(err_neighbor, new_node)
        self.network[err_neighbor][new_node]['age'] = 0

    #stimulate graph using underlying data -- point param
    def fit(self, point):
        #search for nearest neighbors
        [(b0, b0_e),(b1, b1_e)] = self.error_fn(self.network.nodes(), mode="min", locality = point, size=2)

        #increment the age of the edges in the network
        increment_edge_ages(b0)

        #update errors of the two nodes
        self.network[b0]['error'] = self.network[b0]['error'] + b0_e
        self.network[b1]['error'] = self.network[b1]['error'] + b1_e

        #add the edge, will be ignored if it is already in the graph
        #set the edge age to be 0 if it didn't exist
        if not (b0, b1) in self.network.edges():
            self.network.add_edge(b0, b1)
            self.network[b0][b1]['age'] = 0

        #pull nodes in direction of stimulation
        for node in self.network.neighbors(b0):
            new_node = self.node_generator(mode = "average", x = node, y = point, x_weight = 1-self.learning_rate, y_weight = self.learning_rate)
            node.attributes = new_node.attributes
 #           self.network.set_node_attributes(node, new_node.attributes)

        #decrease all node error
        decrease_error()
                
    def increment_edge_ages(node):
        for (f,t) in self.network.edges_iter(node):
            self.network[node][t]['age'] = self.network[node][t]['age'] + 1
            if self.network[n][t]['age'] > self.age_max:
                self.network.remove_edge(n, t)
            if len(self.network.neighbors(n)) == 0:
                self.network.remove_node(n)


    def decrease_error():
        for node in self.network.nodes_iter():
            err = self.network.get_node_attributes('error') * self.learning_rate
            self.network.set_node_attributes(node, 'error', err)

