import urllib2 as url_query


class finviz_query(object):
    '''
       TODO: Class documentation
    '''
    page = "http://finviz.com/export.ashx?v=111&t="

    def __init__(self, symbol):
        self.symbol = symbol
        query = self.page + self.symbol
        data_raw = url_query.urlopen(query).read()
        lines = data_raw.splitlines()
        tuples = zip(lines[0].split(','), lines[1].split(','))
        
        self.data = dict(tuples)

    def return_keys(self):
        return self.data.keys()

    def query(self, key):
        return self.data[key]


# test = finviz_query("bbep")
# for i in test.return_keys():
#    print i, test.query(i)
