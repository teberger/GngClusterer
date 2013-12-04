import glob
import gng
import stock_functions
import file_query
import time
import constants
import sys

if __name__ == '__main__':
    output_file = open(sys.argv[1], 'w')
    stocks = glob.glob("../data/*.csv")
    print 'reading stocks... This may take some time...'
    generators = []
    for stock in stocks:
        generators.append(file_query.stock_data_generator(stock_name = stock,
                                                     initial_day = "1996-04-12",
                                                     window_size = constants.win_size))
    print 'Complete.'

    day = time.strptime( "1996-04-12", "%Y-%m-%d")
    max_day =time.strptime("2013-7-30", "%Y-%m-%d")

    d1 = timedelta(days=1)

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

    initial_vectors = map(lambda x: x.generate(), generators)
    #initial iterationation to semi-fit the data
    print "Initial fit:"
    for i in xrange(init_iterations):
        print "\tIteration ", str(i)
        for vector in initial_vectors:

            #if we don't have sufficient data, ignore the point for this iteration
            if len(vector) < constants.win_size:
                continue
            stock = stock_functions.generate_stats(vector) #TODO

            gng_net.fit(stock)

            iteration = iteration + 1
            if iteration % epoch_lambda == 0:
                gng_net.grow()

    print "Initial fit ended. Beginning clustering..."
    # reset iterationation count
    iteration = 0

    while day < max_day:
        print "Starting ", day.strftime("%Y-%m-%d")
        #iterationate until day == max_day, letting the GNG_NET
        #fit for up to 40000 generations before starting 
        #the iterationation.
        for stock in generators:
            vector = stock_functions.generate_stats(stock.generate())
            if len(vector) < constants.win_size:
                continue
            iteration = iteration + 1
            gng_net.fit(vector)

            if iteration % epoch_lambda == 0:
                gng_net.grow()

        #on each iterationation BFS to find the forests in the
        #GNG_NET, output to file the stocks that are grouped 
        #together
        components = networkx.connected_components(gng_net.network)
        output = ''
        for c in components:
            output = output + '['
            for node in c:
                for v in node.assigned_signals:
                    output = output + str(v) + ','
            output = output + ','

        output_file.write(output + '\n')

        #reset node assignments in GNG_NET
        day = d1 + day

    
