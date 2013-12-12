import glob
import gng
import stock_functions
import file_query
from datetime import datetime, timedelta
import constants
import sys
import networkx
from sets import Set

if __name__ == '__main__':
    output_file = open(sys.argv[1], 'w')
    error_file =  open('err_' + sys.argv[1],  'w')
    stocks = glob.glob("../data/*.csv")
    print 'reading stocks... This may take some time...'
    generators = []
    output = {}
    for stock in stocks:
        print str(len(generators))
        g = file_query.stock_data_generator(stock_name = stock,
                                             initial_day = "1996-04-12",
                                             end_day = "2013-7-30",
                                             window_size = constants.win_size)
        generators.append(g)
        
        output[g.stock_name] = {}
    print 'Complete.'

    #prime the output dictionary
    for i in xrange(len(generators)):
        for h in xrange(len(generators)):
            output[generators[i].stock_name][generators[h].stock_name] = 0

    day = datetime.strptime("1996-04-12", "%Y-%m-%d")
    max_day = datetime.strptime("2013-7-30", "%Y-%m-%d")

    d1 = timedelta(days=7)

    print 'Constructing GNG intial network...'
    #construct GNG_NET
    gng_net = gng.gng(error_fn = stock_functions.lp_distance, 
                      node_gen = stock_functions.generate,
                      learning_rate = constants.learning_rate,
                      age_max = constants.age_max)

    iteration = 0 
    epoch_lambda = constants.epoch_lambda
    init_iterations = constants.target_init_iterations / len(generators)

    print 'Complete...'
    print 'Generating initial vectors'
    
    #initial iterationation to semi-fit the data
    print "Initial fit:"
    for i in xrange(init_iterations):
        print "\tIteration ", str(i), 'Day: ', day.strftime('%Y-%m-%d')
        for g in generators:
            vector = g.generate()
            #if we don't have sufficient data, ignore the point for this iteration
            if len(vector) < constants.num_cross_sections:
                continue
            stock = stock_functions.generate_trend_stats(vector, day)
            if len(stock) != len(constants.stats_keys):
                continue

            gng_net.fit(stock, g.stock_name)
            
            if i % epoch_lambda == 0:
                gng_net.grow()
        day = day + d1
    
    print "Initial fit ended. Beginning clustering..."

    #reset the day
    day = datetime.strptime("1996-04-12", "%Y-%m-%d")

    #reset assigned node sets
    for i in gng_net.network.nodes():
        i.assigned_signals.clear()

    for i in generators:
        i.reset()

    # reset iterationation count
    iteration = 0
    error_file.write('iteration, error')

    #iterate until day >= max_day
    while day < max_day:
        print "Starting ", day.strftime("%Y-%m-%d")
        print '\tNodes:', str(len(gng_net.network.nodes()))
        print '\tComponents:', str(len(networkx.connected_components(gng_net.network)))

        for g in generators:
            #if we don't have sufficient data, ignore the point for this iteration
            vector = g.generate()

            if len(vector) < constants.num_cross_sections:
                continue

            stock = stock_functions.generate_trend_stats(vector, day)

            if len(stock) != len(constants.stats_keys):
                continue

            gng_net.fit(stock, g.stock_name)
            error_file.write(str(iteration) + ',' + str(sum(map(lambda x: x.error, gng_net.network.nodes()))/ float(len(gng_net.network.nodes()))))
            error_file.write('\n')

            iteration = iteration + 1
            if iteration % epoch_lambda == 0:
                gng_net.grow()

        #on each iterationation BFS to find the forests in the
        #GNG_NET, output to file the stocks that are grouped 
        #together
        components = networkx.connected_components(gng_net.network)
        if len(components) > 1:
            for c in components:
                for node in c:
                    for to_node in c:
                        for v in node.assigned_signals:
                            for u in to_node.assigned_signals:
                                output[v][u] = output[v][u] + 1
                    node.assigned_signals.clear()

        #reset node assignments in GNG_NET
        day = d1 + day
    
    sorted_keys = sorted(output.keys())
#    for key in sorted_keys:
#        output_file.write(str(key) + ',')

#    output_file.write('\n')
    

    listed = []
    for key1 in sorted_keys:
#        output_file.write(str(key1) + ',')
        for key2 in sorted_keys:
            if key1 != key2:
                if output[key1][key2] != 0:
                    listed.append((key1, key2, output[key1][key2]))
            else:
                listed.append((key1, key2, 0))
#            if output[key1][key1] == 0:
#                output_file.write('0,')
#            else:
#                output_file.write(str(output[key1][key2] / float(output[key1][key1])) + ',')

    sorted_out = sorted(listed, lambda x,y : cmp(y[2], x[2]))
    output_file.write('\n'.join(map(lambda x: str(x), sorted_out)))
