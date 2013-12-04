from datetime import datetime, timedelta, time

header_items = 'Open,High,Low,Close,Volume,Adj Close'


#generator that slices on the start day, and only generates a new window
#when the next date is valid. 
class stock_data_generator(object):

    def __init__(self, stock_name, initial_day, window_size):
        self.stock_name = stock_name[0 : len(stock_name) - len('.csv')]
        self.stock_name = self.stock_name[self.stock_name.rfind('/') + 1:]
        self.curr_day = datetime.strptime(initial_day, "%Y-%m-%d")
        self.n = window_size
        raw = open(stock_name, 'r')
        lines = raw.read().splitlines()
        self.min_day = datetime.strptime(lines[1].split(',')[0], "%Y-%m-%d")
        self.max_day = datetime.strptime(lines[len(lines)-1].split(',')[0], "%Y-%m-%d")

        print 'Constructing generator for: ', self.stock_name
        print '\tParsing data...'
        self.data = {}
        for l in lines:
            if l == lines[0]:
                continue
            [key,val] = l.split(',', 1)
            self.data[datetime.strptime(key, "%Y-%m-%d")] = dict(zip(header_items.split(','), map(lambda x: float(x), val.split(','))))
        print 'Done...'
        
    def generate(self, start_day, end_day):
        # day deltas
        d1 = timedelta(days=1)
        delta = timedelta(days=self.n)

        window = {}

        self.curr_day = start_day
        while self.curr_day < end_day:
            if self.curr_day in self.data.keys():
                 window[self.curr_day] = self.data[self.curr_day]
            self.curr_day = self.curr_day + d1

        return window
        
