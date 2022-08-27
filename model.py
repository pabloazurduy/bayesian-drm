import numpy as np 
from scipy.stats import truncnorm 

# simulation 
# let's assume a very simplistic model:  spend = \beta*offers + \base_spend + sigma 
num_clients = 1000 
b_spend_pop_mean = 0.5 # \beta_off
spend_pop_min = 0 # usd/week
spend_pop_max = 30 # usd/week
spend_pop_trunc = 2 # lowest billing
beta_off = np.random.exponential(scale=1/b_spend_pop_mean,  # this is the actual beta mean for each client
                                 size=num_clients)
beta_spend = truncnorm.rvs(a = spend_pop_min, 
                           b = spend_pop_max, 
                           size=num_clients)

# simulate weeks ab promos 
weeks = 8 
# test_weeks = ?
low_size  = 100  # low cohort size 
high_size = 100  # high cohort size 
promo_low  = 1.0 
promo_high = 1.2 
promo_control = 0
promo = np.zeros(shape=(num_clients,weeks))
promo[0:low_size,:] = promo_low
promo[low_size:low_size+high_size,:] = promo_high
[*map(np.random.shuffle, promo.T)] #shuffle rows inside columns 
# estimate the raw spend 
spend = truncnorm.rvs(a=spend_pop_min,
                         b=spend_pop_max, 
                         loc = promo*beta_off[:, None] + beta_spend[:, None] # this parameter shift the mean
                         )
# truncate values to lowest billing possible
spend[spend <= spend_pop_trunc] = 0 
# plot
# import matplotlib.pyplot as plt
# plt.hist(spend.flatten(), bins='auto')

