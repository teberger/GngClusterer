from random import *
from numpy import sqrt

'''
    setup the dictionary keys for the stats object
'''
number_of_cross_sections = 7
stats_keys = ['trend', 'norm_trend_mag', 'volatility']
#Sets up the normalized cross sectionals of the data
for i in xrange(number_of_cross_sections):
    stats_keys.append('norm_cross_' + str("%03d") % i)

'''
    Defining the generating function as a modular function
    with two separate operations. See random_node() and average()
'''
def generate(mode, x, y, x_weight = 0.5, y_weight = 0.5):
    if mode == 'random':
        return random_node()
    elif mode == 'average':
        if abs(1 - x_weight - y_weight) > 0.001:
            raise ValueError(x_weight, y_weight, "do not add to 1")
        return average(x, y, x_weight, y_weight)
    else:
        return None

def random_node():
    attr = {}
    attr['trend'] = randint(0,2) - 1
    #positive value, coud be any range including infinity... This may be trouble...
    attr['volatility'] = randuniform(0, 100)
    for key in stats_keys:
        if key == 'trend' or key == 'volatility':
            continue
        #95% of the data should fall between here
        #so this should be a reasonable range to generate
        #from
        attr[key] = randuniform(-2,-2) 

    return node(atrr)

def average(x, y, x_weight, y_weight):
    attr = {}
    if x_weight < y_weight:
        attr['trend'] = y.attributes['trend']
    else:
        attr['trend'] = x.attributes['trend']

    for key in stats_keys:
        if key == 'trend':
            continue
        attr[key] = x.attributes[key] * x_weight + y.attributes[key] * y_weight

    return node(attr)


##Error function
''' 
    return a sorted list of tuples [(node, error of the node)]
    by the error of the node. 
'''
def lp_distance(nodes, x, size = 1, p = 2):
    ret = []
    for i in nodes:
        error = sqrt(sum([(i.attributes[att] - x.attributes[att])**p
                          for att in x.attributes if att != 'trend']))
        #handle trend differently, since it is a determining factor
        #in similarity, it operates on the entire error and magnifies
        #it if the two stock are not following the same trend
        if x.attributes['trend'] != i.attributes['trent']:
            if abs(x.attributes['trend'] - i.attributes['trend']) > 1:
                error = error * 1.5
            else:
                error = error * 1.25
            
        ret + (i, error)

    #slice the data according to the size of the list we need
    return ret.sort(lambda tup: tup[2])[0:size]
        

#leaving this out for now, might not need it
#id_val_counter = 0

class node(object):
    def __init__(self, dictionary):
        for key in stats_keys:
            if not key in dictionary:
                raise ValueError(key)
# See above
#        self.id_val = id_val_counter + 1
#        id_val_counter = self.id_val
        self.attributes = dictionary
