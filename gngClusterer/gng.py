import networkx as nx
import random
from sets import Set

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
        self.network.add_edge(rand_point_x, rand_point_y, weight = 0)
#        self.network[rand_point_x][rand_point_y]['age'] = 0

    def grow(self): 
        
        #get the node with the highest error
        err_node = sorted(self.network.nodes(),
                          lambda x,y: cmp(x.error, y.error)
                         )
        if len(err_node) <= 0:
            print str(self.network.nodes())

        err_node = err_node[0]
        err = err_node.error

        #get its neighboring node with the highest error
        err_neighbor = sorted(self.network.neighbors(err_node),
                              lambda x,y: cmp(x.error, y.error)
                             )

        if len(err_neighbor) <= 0:
            print str(self.network.neighbors(err_node))
            print str(self.network.nodes())
        err_neighbor = err_neighbor[0]
        err_n = err_neighbor.error

        #delete edge between the two
        self.network.remove_edge(err_node, err_neighbor)

        #insert new node
        new_node = self.node_generator(mode = "average", x = err_node.attributes, y = err_neighbor.attributes)
        #update local error of the largest nodes
        err_node.error = err_node.error * (1-self.learning_rate)
        err_neighbor.error = err_neighbor.error * (1-self.learning_rate)
        new_node.error = (err + err_n)/2.0

        #connect to other two nodes with highest error
        self.network.add_node(new_node)
        self.network.add_edge(err_node, new_node, weight=0)
        self.network.add_edge(err_neighbor, new_node, weight=0)


    #stimulate graph using underlying data -- point param
    def fit(self, point, name):
        #search for nearest neighbors
        [(b0, b0_e),(b1, b1_e)] = self.err_fn(self.network.nodes(), x = point, size=2)

        #assign the point to a node in the GNG
        b0.assigned_signals.add(name)

        #increment the weight of the edges in the network
        self.increment_edge_ages(b0)

        #update errors of the two nodes
        b0.error = b0.error + b0_e
        b1.error = b1.error + b1_e

        #add the edge, will be ignored if it is already in the graph
        #set the edge weight to be 0 if it didn't exist
        if (b0, b1) not in self.network.edges():
            self.network.add_edge(b0, b1, weight=0)
#            self.network[b0][b1]['weight'] = 0

        #pull nodes in direction of stimulation
        for node in self.network.neighbors(b0):
            new_node_attr = self.node_generator(mode = "average",
                                                x = node.attributes,
                                                y = point, 
                                                x_weight = 1-self.learning_rate,
                                                y_weight = self.learning_rate)
            #replace node attributes with the averaged attributes
            node.attributes = new_node_attr.attributes

        #decrease all node error
        self.decrease_error()
                
    def increment_edge_ages(self, node):

        for (u,v,data) in self.network.edges_iter(data=True):
            age = data['weight']
            self.network[u][v]['weight'] = age + 1

            if (age + 1) > self.age_max:
                self.network.remove_edge(u, v)
            if len(self.network.neighbors(v)) == 0:
                self.network.remove_node(v)
            if len(self.network.neighbors(u)) == 0:
                self.network.remove_node(u)


    def decrease_error(self):
        for node in self.network.nodes_iter():
            err = node.error * (1 - self.learning_rate)
            node.error = err

