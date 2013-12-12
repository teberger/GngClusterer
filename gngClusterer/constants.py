

win_size = 30 #three month window size

learning_rate = 0.1
age_max = 50
epoch_lambda = 25

target_init_iterations = 20000


'''
    setup the dictionary keys for the stats object
'''
num_cross_sections = 4
stats_keys = []

#Sets up the normalized cross sectionals of the data
for i in xrange(num_cross_sections):
    stats_keys.append('norm_cross_' + str("%03d") % i)
