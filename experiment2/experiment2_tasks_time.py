import numpy as np
from pygame import transform

import matplotlib.pyplot as plt
import utilityFunctions



# Load from .txt files the data
teleop_trial_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_teleop_start.txt', delimiter=',', names=True)
teleop_secondary_task_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_teleop_secondary_start.txt', delimiter=',', names=True)
teleop_secondary_task_ended = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_teleop_secondary_ended.txt', delimiter=',', names=True)

auto_trial_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_auto_start.txt', delimiter=',', names=True)
auto_secondary_task_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_auto_secondary_start.txt', delimiter=',', names=True)
auto_secondary_task_ended = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_auto_secondary_ended.txt', delimiter=',', names=True)

HI_trial_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_HI_start.txt', delimiter=',', names=True)
HI_secondary_task_start = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_HI_secondary_start.txt', delimiter=',', names=True)
HI_secondary_task_ended = np.genfromtxt('/home/manolis/Dropbox/experiment2_data/21_HI_secondary_ended.txt', delimiter=',', names=True)


# calculate teleop
teleop_trial_start['time'] /= 10 ** 9                # keeping only the seconds and throwing the nsec.
teleop_trial_start['time'] = np.round(teleop_trial_start['time'])

teleop_secondary_task_start['time'] /= 10 ** 9
teleop_secondary_task_start['time'] = np.round(teleop_secondary_task_start['time'])

teleop_secondary_task_ended['time'] /= 10 ** 9
teleop_secondary_task_ended['time'] = np.round(teleop_secondary_task_ended['time'])

teleop_primary_completion_time = teleop_trial_start['time'][1] - teleop_trial_start['time'][0]
teleop_secondary_task_time_first = teleop_secondary_task_ended['time'][0] - teleop_secondary_task_start['time'][0]
teleop_secondary_task_time_second = teleop_secondary_task_ended['time'][1] - teleop_secondary_task_start['time'][1]
teleop_secondary_task_total_time = (teleop_secondary_task_time_second+teleop_secondary_task_time_first)

# calculate auto
auto_trial_start['time'] /= 10 ** 9
auto_trial_start['time'] = np.round(auto_trial_start['time'])

auto_secondary_task_start['time'] /= 10 ** 9
auto_secondary_task_start['time'] = np.round(auto_secondary_task_start['time'])

auto_secondary_task_ended['time'] /= 10 ** 9
auto_secondary_task_ended['time'] = np.round(auto_secondary_task_ended['time'])

auto_primary_completion_time = auto_trial_start['time'][1] - auto_trial_start['time'][0]
auto_secondary_task_time_first = auto_secondary_task_ended['time'][0] - auto_secondary_task_start['time'][0]
auto_secondary_task_time_second = auto_secondary_task_ended['time'][1] - auto_secondary_task_start['time'][1]
auto_secondary_task_total_time = (auto_secondary_task_time_second+auto_secondary_task_time_first)

# calculate HI
HI_trial_start['time'] /= 10 ** 9
HI_trial_start['time'] = np.round(HI_trial_start['time'])

HI_secondary_task_start['time'] /= 10 ** 9
HI_secondary_task_start['time'] = np.round(HI_secondary_task_start['time'])

HI_secondary_task_ended['time'] /= 10 ** 9
HI_secondary_task_ended['time'] = np.round(HI_secondary_task_ended['time'])

HI_primary_completion_time = HI_trial_start['time'][1] - HI_trial_start['time'][0]
HI_secondary_task_time_first = HI_secondary_task_ended['time'][0] - HI_secondary_task_start['time'][0]
HI_secondary_task_time_second = HI_secondary_task_ended['time'][1] - HI_secondary_task_start['time'][1]
HI_secondary_task_total_time = (HI_secondary_task_time_second+HI_secondary_task_time_first)




print ('Teleop: Primary task completion time: %s' % teleop_primary_completion_time)
print ('Teleop: Secondary task completion time 1st: %s' % teleop_secondary_task_time_first)
print ('Teleop: Secondary task completion time 2nd: %s' % teleop_secondary_task_time_second)
print ('Teleop: Secondary task completion time total: %s' % teleop_secondary_task_total_time)

print ('Auto: Primary task completion time: %s' % auto_primary_completion_time)
print ('Auto: Secondary task completion time 1st: %s' % auto_secondary_task_time_first)
print ('Auto: Secondary task completion time 2nd: %s' % auto_secondary_task_time_second)
print ('Auto: Secondary task completion time total: %s' % auto_secondary_task_total_time)

print ('HI: Primary task completion time: %s' % HI_primary_completion_time)
print ('HI: Secondary task completion time 1st: %s' % HI_secondary_task_time_first)
print ('HI: Secondary task completion time 2nd: %s' % HI_secondary_task_time_second)
print ('HI: Secondary task completion time total: %s' % HI_secondary_task_total_time)



44