from itertools import count

__author__ = 'manolis'

import numpy as np


def CalibrateTimeAndRt(offsetTime, rtData):

    offsetTime['time'] /= 10 ** 9         # keeping only the seconds and throwing the nsec.
    offsetTime = round(offsetTime['time'])
    timeOfRT = rtData['time']
    timeOfRT /= 10 ** 9
    timeOfRT = np.round(timeOfRT)
    timeOfRT -= offsetTime
    RT = np.round(rtData['fielddata'], 3)  # keeping only 3 significant digits for RT

    return (timeOfRT, RT)


# It has some data read from numpy from ROS and keeps + shifts them into 0-end of trial interval.
def timeShiftData(trial_time_data = np.array, data = np.array, data_time_label ='time', data_field_label = 'put here label'):

    time = []
    temp_data = []

    for i in range(0, data[data_time_label].size):

        if (data[data_time_label][i] >= trial_time_data['time'][0]) and (data[data_time_label][i] <= trial_time_data['time'][1]):

            time.append(round(data[data_time_label][i] - trial_time_data['time'][0],3))
            temp_data.append(round(data[data_field_label][i],3))


    data_shifted = np.array([time,temp_data])
    return (data_shifted)


# augments size of a data array to match this of error sampling rate
def augmentSize(data_to_augment = np.array, error_time_data = np.array, sampling_time = float):

    augmented_array = np.array( np.zeros( (2, error_time_data.size) ) )
    augmented_array[0] = error_time_data  # putting the times to augemneted array
    sampling_ticks = np.round(np.divide(data_to_augment[0], sampling_time)) # time->sampling ticks transform

    for i in range(0, sampling_ticks.size):
        augmented_array[1][sampling_ticks[i]] = data_to_augment[1][i]

    return augmented_array


# calculates the exponential moving average
def expMovingAverage (raw_error= np.array, initialization_steps = int, alpha = float):

    count_timesteps = 1
    error_sum = 0
    error_average = np.array( np.zeros( (2,raw_error[0].size) ) )

    for i in range(0, raw_error[0].size):

      if (count_timesteps <= initialization_steps):
        error_sum += raw_error[1][i]
        error_average[1][i] = error_sum / count_timesteps
        count_timesteps += 1
      else:
        error_average[1][i] = alpha * raw_error[1][i] + (1- alpha) * error_average[1][i-1]

    error_average[0] = raw_error[0]
    return error_average


# implimentation of the threshold controller
def thresholdController(moving_average = np.array, threshold = float ):

    change_loa = np.array( np.zeros( (2,moving_average[0].size) ) )
    count = 25

    for i in range(75, (moving_average[0].size-25) ): # ignoring first 15 sec and last 5 sec, sampling was 0.2, (15/0.2  = 75 steps)

         if (moving_average[1][i] >= threshold and count>=25):

            change_loa[1][i] = 1
            count = 0

         count +=1


    change_loa[0] = moving_average[0]

    return change_loa


# the cost/objective/loss fuction to compute optimization, currenty sum of absolute error/loss
def lossFunction(loa_prediction = np.array, loa_operator =np.array):

    total_cost = []
    time_min_found = 0
    time_ticks_offset = 25 # offset +- 5 sec from the prediction in ticks of 0.2sec
    penalty_no_predictions = 100000000000000000000000 # penalty in case no predictions are made
    penalty_no_matching = 6   # penalty for the predictions that do not match HI

    if ( sum(loa_prediction[1]) >=2 ):

        for i in range(0, loa_prediction[0].size):

          if (loa_prediction[1][i] == 1):

              time_prediction = i
              time_distance_min = time_ticks_offset + 5
              match_found = 0  # denotes if a HI match is found for a prediction LOA change

              for j in range(time_prediction-time_ticks_offset, time_prediction+time_ticks_offset): # just look +- 5 sec from the prediction

                  if (loa_operator[1][j]==1):
                      time_distance = abs(time_prediction - j) # the absolute distance in time between predition and human LOA change
                      match_found = 1
                      if (time_distance < time_distance_min):
                          time_distance_min = time_distance
                          match_found = 1

              if (match_found == 1):
                  total_cost.append(time_distance_min)
              else:
                  total_cost.append(penalty_no_matching)

        total_cost = np.sum( np.array(total_cost) ) * 0.2

    else:
        total_cost = penalty_no_predictions

    return total_cost


# grid search
def gridSearch(a_start= float, a_end = float, thres_start=float, thres_end=float, sampling_time = float,  raw_error= np.array,
               initialization_steps = int, loa_operator =np.array):

    check_cost = []
    smoothed_error = expMovingAverage(raw_error, initialization_steps, 0.04) # just once to allow for augmenting the loa operator changes
    loa_operator = augmentSize(loa_operator, smoothed_error[0], sampling_time)
    best_cost = 100000000000
    a_iteration_array = np.arange(a_start, a_end+0.01, 0.01)
    thres_iteration_array = np.arange(thres_start, thres_end+0.01, 0.01)

    for a in a_iteration_array:

        smoothed_error = expMovingAverage(raw_error, initialization_steps, a)

        for thres in thres_iteration_array:

           loa_prediction = thresholdController(smoothed_error, thres)
           cost = lossFunction(loa_prediction, loa_operator)


           if (cost < best_cost):

                best_cost = cost
                check_cost.append(best_cost)
                best_a = a
                best_thres = thres

    return [best_a, best_thres, best_cost, check_cost]



