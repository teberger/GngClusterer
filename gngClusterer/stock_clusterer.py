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
    stocks = glob.glob("../data/*.csv")
    print 'reading stocks... This may take some time...'
    generators = []
    for stock in stocks:
        print str(len(generators))
        generators.append(file_query.stock_data_generator(stock_name = stock,
                                                     initial_day = "1996-04-12",
                                                     end_day = "2013-7-30",
                                                     window_size = constants.win_size))
    print 'Complete.'

    day = datetime.strptime("1996-04-12", "%Y-%m-%d")
    max_day = datetime.strptime("2013-7-30", "%Y-%m-%d")

    d1 = timedelta(days=1)
    dn = timedelta(days=constants.win_size)

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
        print "\tIteration ", str(iteration), 'Day: ', day.strftime('%Y-%m-%d')
        for g in generators:
            vector = g.generate()
            #if we don't have sufficient data, ignore the point for this iteration
            if len(vector) < constants.num_cross_sections:
                continue
            stock = stock_functions.generate_stats(vector, day)
            if len(stock) != len(constants.stats_keys):
                continue

            gng_net.fit(stock, g.stock_name)

            iteration = iteration + 1
            if iteration % epoch_lambda == 0:
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

    while day < max_day:
        if day.day == 1:
            print "Starting ", day.strftime("%Y-%m-%d")
        #iterationate until day == max_day, letting the GNG_NET
        #fit for up to 40000 generations before starting 
        #the iterationation.
        for g in generators:
            #if we don't have sufficient data, ignore the point for this iteration
            vector = g.generate()

            if len(vector) < constants.num_cross_sections:
                continue

            stock = stock_functions.generate_stats(vector, day)

            if len(stock) != len(constants.stats_keys):
                continue

            gng_net.fit(stock, g.stock_name)

            iteration = iteration + 1
            if iteration % epoch_lambda == 0:
                print 'Growing...'
                print '\tNodes:', str(len(gng_net.network.nodes()))
                print '\tComponents:', str(len(networkx.connected_components(gng_net.network)))
                gng_net.grow()

        #on each iterationation BFS to find the forests in the
        #GNG_NET, output to file the stocks that are grouped 
        #together
        components = networkx.connected_components(gng_net.network)
        output = day.strftime('%Y-%m-%d') + ','
        for c in components:
            output = output + '['
            for node in c:
                for v in node.assigned_signals:
                    output = output + str(v) + ','
                node.assigned_signals.clear()
            output = output + '],'

        output_file.write(output + '\n')

        #reset node assignments in GNG_NET
        day = d1 + day

    
