from random import *

'''
    setup the dictionary keys for the stats object
'''
number_of_cross_sections = 7
stats_keys = ['trend', 'norm_trend_mag', 'volatility']
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
    #positive value, coud be any range including infinity...
    attr['volatility'] = randuniform(0, 100)
    for key in stats_keys:
        if key == 'trend' or key == 'volatility':
            continue
        #95% of the data should fall between here
        #so this should be a reasonabl range to generate
        #from
        attr[key] = randuniform(-2,-2) 

    return node(atrr)

def average(x, y, x_weight, y_weight):
    attr = {}
    if x_weight < y_weight:
        attr['trend'] = y_weight
    else:
        attr['trend'] = x_weight

    for key in stats_keys:
        if key == 'trend':
            continue
        attr[key] = x.attributes[key] * x_weight + y.attributes[key] * y_weight

    return node(attr)


'''
    Testing functionality
'''
if __name__ == '__main__':
    for i in xrange(100):
        print randint(0,2)-1

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
