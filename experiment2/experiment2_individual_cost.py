import utilityFunctions as uf
import numpy as np
import matplotlib.pyplot as plt


sampling_time = 0.2
control_threshold = 0.07
alpha = 0.06
initializing_steps = 25

# Load from .txt files the data
vel_error = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/linear_vel_error/13_HI_linear_vel_error.txt', delimiter=',', names=True)
#cmd_vel = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/03_HI_cmd_vel.txt', delimiter=',', names=True)
loa_has_changed = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/loa_changed/13_HI_loa_changed.txt', delimiter=',', names=True)
trial_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/trial_start/13_HI_start.txt', delimiter=',', names=True)


# keep only secs and msecs
trial_start['time'] /= 10 ** 9
trial_start['time'] = np.round(trial_start['time'], 3)
vel_error['time'] /= 10 ** 9
vel_error['time'] = np.round(vel_error['time'], 3)
#cmd_vel['time'] /= 10 ** 9
#cmd_vel['time'] = np.round(cmd_vel['time'], 3)
loa_has_changed['time'] /= 10 ** 9
loa_has_changed['time'] = np.round(loa_has_changed['time'], 3)



vel_error = uf.timeShiftData(trial_start, vel_error, data_time_label= 'time', data_field_label='fielddata')
#linear_vel = uf.timeShiftData(trial_start, cmd_vel, data_time_label= 'time', data_field_label='fieldlinearx')
loa_has_changed = uf.timeShiftData(trial_start, loa_has_changed, data_time_label= 'time', data_field_label='fielddata')
#angular_vel = uf.timeShiftData(trial_start, cmd_vel, data_time_label= 'time', data_field_label='fieldangularz')
smoothed_error = uf.expMovingAverage(vel_error, initializing_steps, alpha)
loa_has_changed = uf.augmentSize(loa_has_changed, smoothed_error[0], sampling_time)

loa_prediction_thres = uf.thresholdController(smoothed_error, control_threshold)
cost_thres = uf.lossFunction(loa_prediction_thres, loa_has_changed)

loa_prediction_fuzzy = uf.fuzzyController(smoothed_error)
cost_fuzzy = uf.lossFunction(loa_prediction_fuzzy, loa_has_changed)

print ('cost thres', cost_thres)
print ('cost fuzzy', cost_fuzzy)

# PLOTing
plt.plot(vel_error[0], vel_error[1], label='vel_error', color='r')
plt.plot(smoothed_error[0], smoothed_error[1], label='smoothed error', color='c')
plt.bar(loa_has_changed[0], loa_has_changed[1], label='LOA change', width=0.5, color= 'g')
plt.bar(loa_prediction_thres[0], loa_prediction_thres[1], label = 'LOA prediction', width = 0.5, color='black')
plt.title('blabla')
plt.xlabel('time (sec)')
plt.ylabel('error and actual velocity (m/s')
plt.legend()
#plt.show()



