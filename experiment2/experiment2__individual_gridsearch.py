import utilityFunctions as uf
import numpy as np
import matplotlib.pyplot as plt


sampling_time = 0.2
a_start = 0.01
a_end = 0.1
thres_start = 0.05
thres_end = 0.4
initializing_steps = 10

# Load from .txt files the data
raw_vel_error = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/02_HI_vel_error.txt', delimiter=',', names=True)
cmd_vel = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/02_HI_cmd_vel.txt', delimiter=',', names=True)
loa_has_changed = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/02_HI_loa_changed.txt', delimiter=',', names=True)
trial_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/02_HI_start.txt', delimiter=',', names=True)


# keep only secs and msecs
trial_start['time'] /= 10 ** 9
trial_start['time'] = np.round(trial_start['time'], 3)
raw_vel_error['time'] /= 10 ** 9
raw_vel_error['time'] = np.round(raw_vel_error['time'], 3)
cmd_vel['time'] /= 10 ** 9
cmd_vel['time'] = np.round(cmd_vel['time'], 3)
loa_has_changed['time'] /= 10 ** 9
loa_has_changed['time'] = np.round(loa_has_changed['time'], 3)


raw_vel_error = uf.timeShiftData(trial_start, raw_vel_error, data_time_label= 'time', data_field_label='fielddata')
loa_has_changed = uf.timeShiftData(trial_start, loa_has_changed, data_time_label= 'time', data_field_label='fielddata')

result = uf.gridSearch(a_start=a_start, a_end=a_end, thres_start= thres_start, thres_end= thres_end,  sampling_time= sampling_time,
                       raw_error=raw_vel_error, initialization_steps=initializing_steps , loa_operator= loa_has_changed   )

print result





