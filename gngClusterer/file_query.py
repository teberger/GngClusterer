import time

header_items = 'Open,High,Low,Close,Volume,Adj Close'


#generator that slices on the start day, and only generates a new window
#when the next date is valid. 
class stock_data_generator(object):

    def __init__(self, stock_name, initial_day, window_size):
        self.stock_name = stock_name[0 : len(stock_name) - len('.csv')]
        self.stock_name = self.stock_name[self.stock_name.rfind('/') + 1:]
        self.curr_day = time.strptime(initial_day, "%Y-%m-%d")
        self.n = window_size
        raw = open(stock_name, 'r')
        lines = raw.read().readlines()
        self.min_day = time.strptime(lines[1].split(',')[0], "%Y-%m-%d")
        self.max_day = time.strptime(lines[len(lines)-1].split(',')[0], "%Y-%m-%d")

        self.data = {}
        for l in lines:
            [key,val] = l.split(',', 1)
            data[key] = dict(zip(header_items.split(','), map(lambda x: float(x), val.split(','))))
        
    def generate():
        # day deltas
        d1 = timedelta(days=1)
        delta = timedelta(days=n)

        window = {}
        i = 0
        while len(window) < self.n and (self.curr_day >= self.min_day and self.curr_day + timedelta(days=i) <= self.max_day):
             i_d = timedelta(days=i)
             if self.curr_day + i_d in self.data.keys():
                 window[self.curr_day + i_d] = self.data[self.curr_day + i_d]
             i = i + 1
        self.curr_day = self.curr_day + d1
        return window
        
