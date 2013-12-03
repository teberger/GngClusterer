import glob
import gng
import stock_functions
import time
import constants

if __name__ == '__main__':
    stocks = glob.glob("../data/*.csv")
    generators = []
    for stock in stocks:
        generators + file_query.stock_data_generator(stock_name = stock,
                                                     initial_day = "1996-04-12",
                                                     window_size = constants.win_size)

    day = time.strptime("%Y-%m-%d", "1996-04-12")
    max_day =time.strptime("%Y-%m-%d", "2013-7-30")

    d1 = timedelta(days=1)

    #construct GNG_NET
    gng_net = gng.gng(error_fn = stock_functions.lp_distance, 
                      node_gen = stock_functions.generate,
                      learning_rate = constants.learning_rate
                      age_max = constants.age_max)

    iteration = 0 
    epoch_lambda = constants.epoch_lambda
    init_iterations = constants.target_init_iterations / len(generators)

    initial_vectors = map(lambda x: x.generate(), generators):
    #initial iterationation to semi-fit the data
    for i in xrange(init_iterations):
        for vector in initial_vectors

            #if we don't have sufficient data, ignore the point for this iteration
            if len(vector) < constants.win_size:
                continue
            stock = None #TODO

            gng_net.fit(stock)

            iteration = iteration + 1
            if iteration % epoch_lambda == 0:
                gng_net.grow()

    # reset iterationation count
    iteration = 0

    while day < max_day:
        #iterationate until day == max_day, letting the GNG_NET
        #fit for up to 40000 generations before starting 
        #the iterationation.
        for stock in generators:
            vector = stock.generate()
            if len(vector) < constants.win_size:
                continue
            iteration = iteration + 1
            gng_net.fit(vector)

            if iteration % epoch_lambda == 0:
                gng_net.grow()

        #TODO
        #on each iterationation BFS to find the forests in the
        #GNG_NET, output to file the stocks that are grouped 
        #together

        #reset node assignments in GNG_NET
        day = d1 + day

    
