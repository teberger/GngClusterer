from datetime import datetime, timedelta, time

header_items = 'Open,High,Low,Close,Volume,Adj Close'

#generator that slices on the start day, and only generates a new window
#when the next date is valid. 
class stock_data_generator(object):

    def __init__(self, stock_name, initial_day, end_day, window_size):
        self.stock_name = stock_name[0 : len(stock_name) - len('.csv')]
        self.stock_name = self.stock_name[self.stock_name.rfind('/') + 1:]

        self.init_day = datetime.strptime(initial_day, '%Y-%m-%d')
        self.day = self.init_day - timedelta(days=window_size)
        self.n = window_size
        raw = open(stock_name, 'r')
        raw_out = open(stock_name + '.seq', 'w')

        print 'Constructing generator for: ', self.stock_name
        print '\tParsing and restructuring data...'

        d1 = timedelta(days = 1)
        end_day = datetime.strptime(end_day, '%Y-%m-%d')
        day = datetime.strptime(initial_day, "%Y-%m-%d") - d1
        #remove header
        line = raw.readline()
        no_data = False
        while day < end_day:

            line = raw.readline()
            if line == '':
                raw_out.write(day.strftime('%Y-%m-%d') + ',NONE\n')
            else: 
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
        self.reset()

        print 'Done...'

    def reset(self):
        self.day = self.init_day - timedelta(days = self.n)
        self.window = []
        self.reader.seek(0)

    def generate(self):
        #remove any that fell off outside the window
        for i in self.window:
            date = datetime.strptime(i[0:i.find(',')], '%Y-%m-%d')
            if date < self.day:
                self.window.remove(i)

        self.day = self.day + timedelta(days = 1)

        #append the next day if it is there
        line = self.reader.readline()

        if ('NONE' not in line) and (line != ""):
            self.window.append(line)

        # return a dictionary of the days we do have
        header = header_items.split(',')
        day_dict = dict(map(lambda x: (x[0:x.find(',')], x[x.find(',')+1:]), self.window))
        
        ret = {}
        for day in day_dict:
            vals = day_dict[day].split(',')
            ret[datetime.strptime(day, '%Y-%m-%d')] = dict(zip(header, map(lambda x: float(x.strip()), vals)))
#        ret = dict(map(lambda x: (x[0:x.find(',')], dict(zip(header_items.split(','), x[x.find(',')+1:].split(',')))), self.window))

        return ret
