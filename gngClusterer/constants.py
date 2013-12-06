

win_size = 90 #three month window size

learning_rate = 0.1
age_max = 200
epoch_lambda = 50

target_init_iterations = 40000


'''
    setup the dictionary keys for the stats object
'''
num_cross_sections = 7
stats_keys = ['trend', 'norm_trend_mag', 'volatility']

#Sets up the normalized cross sectionals of the data
for i in xrange(num_cross_sections):
    stats_keys.append('norm_cross_' + str("%03d") % i)
