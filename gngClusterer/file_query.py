from datetime import datetime, timedelta, time

header_items = 'Open,High,Low,Close,Volume,Adj Close'

#generator that slices on the start day, and only generates a new window
#when the next date is valid. 
class stock_data_generator(object):

    def __init__(self, stock_name, initial_day, end_day, window_size):
        self.stock_name = stock_name[0 : len(stock_name) - len('.csv')]
        self.stock_name = self.stock_name[self.stock_name.rfind('/') + 1:]
        self.init_day = datetime.strptime(initial_day, '%Y-%m-%d')
        self.n = window_size
        raw = open(stock_name, 'r')
        raw_out = open(stock_name + '.seq', 'w')

        print 'Constructing generator for: ', self.stock_name
        print '\tParsing and restructuring data...'

        d1 = timedelta(days = 1)
        end_day = datetime.strptime(end_day, '%Y-%m-%d')
        day = datetime.strptime(initial_day, "%Y-%m-%d")
        #remove header
        line = raw.readline()
        while day < end_day:
            line = raw.readline()
            if line == "":
                raw_out.write(day.strftime('%Y-%m-%d') + ',NONE\n')
                day = day + d1
                continue
            line_date = datetime.strptime(line[0:line.find(',')], '%Y-%m-%d')
            while line_date > day:
                raw_out.write(day.strftime('%Y-%m-%d') + ',NONE\n')
                day = day + d1

            raw_out.write(line)
            day = day + d1
        
        #close the raw file
        raw.close()
        #close this since we only need read in the generating portion of this
        #file
        raw_out.close()
        self.reader = open(stock_name + '.seq', 'r')
        self.window = []
        print 'Done...'

    def reset(self):
        self.window = []
        self.reader.seek(0)

    def generate(self):
        if len(self.window) != 0 and datetime.strptime(self.window[0][0:self.window[0].find(',')], '%Y-%m-%d') - timedelta(days=self.n) >= self.init_day:
            #remove the first day
            self.window = self.window[1:]

        #append the next day
        line = self.reader.readline()
        if ('NONE' not in line) and (line != ""):
            self.window.append(self.reader.readline())

        print str(self.window)

        # return a dictionary of the days we do have
        ret = dict(map(lambda x: (x[0:x.find(',')], dict(zip(header_items.split(','), x[x.find(',')+1:].split(',')))), self.window))
        
        return ret
