

win_size = 30 #One month window size

learning_rate = 0.1
age_max = 201
epoch_lambda = 100

target_init_iterations = 40000


'''
    setup the dictionary keys for the stats object
'''
num_cross_sections = 7
stats_keys = ['trend', 'norm_trend_mag', 'volatility']

#Sets up the normalized cross sectionals of the data
for i in xrange(number_of_cross_sections):
    stats_keys.append('norm_cross_' + str("%03d") % i)
