import time

#generator that slices on the start day, and only generates a new window
#when the next date is valid. 

class stock_data_generator(object):
    file_loc = "../data/"
    def __init__(self, stock_name, initial_day, window_size):
        self.stock_name = stock_name
        self.curr_day = time.strptime("%Y-%m-%d", initial_day)
        self.n = window_size
        raw = open('./data/' + stock_name + '.csv', 'r')
        lines = raw.read().splitlines()
        self.min_day = time.strptime("%Y-%m-%d", lines[0].split(',')[0])
        self.max_day = time.strptime("%Y-%m-%d", lines[len(lines)-1].split(',')[0])

        self.data = {}
        for l in lines:
            [key,val] = l.split(',', 1)
            self.data[key] = val
        

    #Python 3 compatibility
    def __next__():
        return next()

    def next():
        # day deltas
        d1 = timedelta(days=1)
        delta = timedelta(days=n)

        while self.curr_day + delta <= self.max_day:
            window = {}
            i = 0
            while len(window) < self.n and (self.curr_day >= self.min_day and
                                            self.curr_day + timedelta(days=i) <= self.max_day):
                i_d = timedelta(days=i)
                if self.curr_day + i_d in self.data.keys():
                    window[self.curr_day + i_d] = self.data[self.curr_day + i_d]
                i = i + 1
            yield window
            self.curr_day = self.curr_day + d1
