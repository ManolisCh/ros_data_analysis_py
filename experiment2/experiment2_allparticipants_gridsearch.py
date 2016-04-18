import utilityFunctions as uf
import numpy as np
import os
import matplotlib.pyplot as plt


sampling_time = 0.2
a_start = 0.02
a_end = 0.06
thres_start = 0.06
thres_end = 0.1
initializing_steps = 10
best_cost = 100000000000000000

path_vector_error = '/home/manolis/Dropbox/experiment2_data/vector_vel_error/'
path_vel_error = '/home/manolis/Dropbox/experiment2_data/linear_vel_error/'
path_trial_start = '/home/manolis/Dropbox/experiment2_data/trial_start/'
path_loa_changed = '/home/manolis/Dropbox/experiment2_data/loa_changed/'

check_cost = []
a_iteration_array = np.arange(a_start, a_end+0.01, 0.01)
thres_iteration_array = np.arange(thres_start, thres_end+0.01, 0.01)


files_vel_errors = os.listdir(path_vel_error)
files_vel_errors.sort()
files_trial_start = os.listdir(path_trial_start)
files_trial_start.sort()
files_loa_changed = os.listdir(path_loa_changed)
files_loa_changed.sort()



check_cost = []

#return [best_a, best_thres, best_cost, check_cost]


for a in a_iteration_array:

    for thres in thres_iteration_array:

        total_cost_each_param = 0

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
            smoothed_error = uf.expMovingAverage(raw_vel_error, initializing_steps, a)
            loa_operator = uf.augmentSize(loa_has_changed, smoothed_error[0], sampling_time)
            loa_prediction = uf.thresholdController(smoothed_error, thres)
            cost = uf.lossFunction(loa_prediction, loa_operator)
            total_cost_each_param += cost

        if (total_cost_each_param < best_cost):
            best_cost = total_cost_each_param
            check_cost.append(best_cost)
            best_a = a
            best_thres = thres

print('best a=', best_a)
print('best thres = ', best_thres)
print('best cost = ', best_cost)
print('cost check', check_cost)













