from random import *
from numpy import sqrt, ceil
from math import fsum
from sets import Set
import constants


'''
    Defining the generating function as a modular function
    with two separate operations. See random_node() and average()
'''
def generate(mode, x = None, y = None, x_weight = 0.5, y_weight = 0.5):
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
    attr['volatility'] = random()*100
    for key in constants.stats_keys:
        if key == 'trend' or key == 'volatility':
            continue
        #95% of the data should fall between here
        #so this should be a reasonable range to generate
        #from
        attr[key] = random()*2 - 2

    return node(attr)

def average(x, y, x_weight, y_weight):
    attr = {}
    if x_weight < y_weight:
        attr['trend'] = y['trend']
    else:
        attr['trend'] = x['trend']

    for key in constants.stats_keys:
        if key == 'trend':
            continue
        attr[key] = x[key] * x_weight + y[key] * y_weight

    return node(attr)


##Error function
''' 
    return a sorted list of tuples [(node, error of the node)]
    by the error of the node. 
'''
def lp_distance(nodes, x, size = 1, p = 2):
    ret = []
    for i in nodes:
        error = sqrt(sum([(i.attributes[att] - x[att])**p for att in x.keys() if att != 'trend']))
        #handle trend differently, since it is a determining factor
        #in similarity, it operates on the entire error and magnifies
        #it if the two stock are not following the same trend
        if x['trend'] != i.attributes['trend']:
            if abs(x['trend'] - i.attributes['trend']) > 1:
                error = error * 1.5
            else:
                error = error * 1.25
            
        ret.append((i, error))

    #slice the data according to the size of the list we need
    return sorted(ret, lambda x,y: cmp(x[1],y[1]))[0:size]


def generate_stats(day_window, current_day):
    if len(day_window) < constants.num_cross_sections:
        return {}

    stats = {}

    min_day = max_day = day_window.keys()[0]
    x_bar = []
    for key in day_window:
        if min_day > key:
            min_day = key
        if max_day < key:
            max_day = key
        print day_window[key]
        x_bar.append(day_window[key]['Open'])
        x_bar.append(day_window[key]['Close'])

    x_bar = fsum(x_bar) / float(len(x_bar)*2)
    
    var = []
    for key in day_window:
        var.append((day_window[key]['Open'] - x_bar)**2)
        var.append((day_window[key]['Close'] - x_bar)**2)
    var = fsum(var)
    std_dev = sqrt(var)
    stats['trend'] = cmp(day_window[min_day]['Open'] - day_window[max_day]['Close'], 0)

    stats['norm_trend_mag'] = (day_window[min_day]['Open'] - x_bar)/std_dev - (day_window[max_day]['Close'] - x_bar)/std_dev

    if x_bar != 0:
        stats['volatility'] = var / x_bar
    else: 
        stats['volatility'] = -1


    num_days = int(ceil(len(day_window) / float(constants.num_cross_sections)))
    days = sorted(day_window)
    for i in xrange(constants.num_cross_sections):
        sliced = days[i*num_days : (i+1)*num_days]
        if (len(sliced) == 0):
            return {}
        avg = 0
        for d in sliced:
            avg = avg + day_window[d]['Open']
            avg = avg + day_window[d]['Close']
        avg  = avg / float(len(sliced)*2)
        stats[constants.stats_keys[3 + i]] = (avg - x_bar)/std_dev

    return stats

#leaving this out for now, might not need it
#id_val_counter = 0

class node(object):
    def __init__(self, dictionary):
        for key in constants.stats_keys:
            if not key in dictionary:
                raise ValueError(key)
# See above
#        self.id_val = id_val_counter + 1
#        id_val_counter = self.id_val
        self.attributes = dictionary
        self.assigned_signals = Set()
        self.error = 0
