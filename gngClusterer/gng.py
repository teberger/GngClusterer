import networkx as nx
import random

class gng(networkx):
    def __init__(self, error_fn, point_x = [0], point_y = [0]):
        self.err_fn = error_fn
        self.network = nx.Graph(point_x, point_y)
        self.network.add_edge(point_x, point_y)

    def grow(self, backing_graph):
        #find node with highest error -- distance to closest node
        err_node = max_args(error_fn, self.network.nodes())

        #find connected node with highest error
        err_neighbor = max_args(error_fn, self.network.get_edges(err_node))

        #delete edge between the two
        self.network.remove_edge(err_node, err_neighbor)

        #insert new node
        new_node = pass
        #connect to other two nodes with highest error
        self.network.add_edge(err_node, new_node)
        self.network.add_edge(err_neighbor, new_node)

    def fit(self, point):
        #stimulate graph using underlying data -- point param
        #search for nearest neighbors
        #pull nodes in direction of stimulation
        pass


def max_args(fn, *ls, curr = null):
    if fn(ls[0]) > curr:
        return max_args(fn, ls[1:], ls[0])
    else:
        return max_args(fn, ls[1:], curr)
    
