import glob
import gng
import stock_functions
import time

if __name__ == '__main__':
    stocks = glob.glob("../data/*.csv")
    generators = []
    day = time.strptime("%Y-%m-%d", "1996-04-12")
    for stock in stocks:
        generators + file_query.stock_data_generator(stock_name = stock[0:len(stock)-4:-1], 
                                                     initial_day = "1996-04-12",
                                                     window_size = 30)

    max_day =time.strptime("%Y-%m-%d", "2013-7-30")

    #construct GNG

    #iterate until day == max_day, letting the GNG
    #fit for up to 40000 generations before starting 
    #the iteration.

    #on each iteration BFS to find the forests in the
    #GNG, output to file the stocks that are grouped 
    #together

    #reset node assignments in GNG
    
