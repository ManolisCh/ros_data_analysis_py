import utilityFunctions as uf
import numpy as np
import os
import matplotlib.pyplot as plt


sampling_time = 0.2
alpha = 0.06
thres= 0.07
initializing_steps = 25
total_cost_fuzzy = 0
total_cost_thres = 0
count = 0

path_vector_error = '/home/manolis/Dropbox/experiment2_data/vector_vel_error/'
path_vel_error = '/home/manolis/Dropbox/experiment2_data/linear_vel_error/'
path_trial_start = '/home/manolis/Dropbox/experiment2_data/trial_start/'
path_loa_changed = '/home/manolis/Dropbox/experiment2_data/loa_changed/'

files_vel_errors = os.listdir(path_vel_error)
files_vel_errors.sort()
files_trial_start = os.listdir(path_trial_start)
files_trial_start.sort()
files_loa_changed = os.listdir(path_loa_changed)
files_loa_changed.sort()



for i in range( len(files_loa_changed) ):

        # Load from .txt files the data
        raw_vel_error = np.genfromtxt( path_vel_error + files_vel_errors[i], delimiter=',', names=True)
        loa_has_changed = np.genfromtxt(path_loa_changed + files_loa_changed[i], delimiter=',', names=True)
        trial_start = np.genfromtxt(path_trial_start + files_trial_start[i], delimiter=',', names=True)

        # keep only secs and msecs and shift time of data
        trial_start['time'] /= 10 ** 9
        trial_start['time'] = np.round(trial_start['time'], 3)
        raw_vel_error['time'] /= 10 ** 9
        raw_vel_error['time'] = np.round(raw_vel_error['time'], 3)
        loa_has_changed['time'] /= 10 ** 9
        loa_has_changed['time'] = np.round(loa_has_changed['time'], 3)

        raw_vel_error = uf.timeShiftData(trial_start, raw_vel_error, data_time_label='time', data_field_label='fielddata')
        loa_has_changed = uf.timeShiftData(trial_start, loa_has_changed, data_time_label='time', data_field_label='fielddata')
        smoothed_error = uf.expMovingAverage(raw_vel_error, initializing_steps, alpha)
        loa_operator = uf.augmentSize(loa_has_changed, smoothed_error[0], sampling_time)

        loa_prediction_fuzzy = uf.fuzzyController(smoothed_error)
        total_cost_fuzzy += uf.lossFunction(loa_prediction_fuzzy, loa_operator)

        loa_prediction_thres = uf.thresholdController(smoothed_error, thres)
        total_cost_thres += uf.lossFunction(loa_prediction_thres, loa_operator)

        count += 1

        print('Fuzzy cost =', uf.lossFunction(loa_prediction_fuzzy, loa_operator))
        print('Thres cost = ', uf.lossFunction(loa_prediction_thres, loa_operator))
        print count





print('Fuzzy total cost =', total_cost_fuzzy)
print('Thres total cost = ', total_cost_thres)














