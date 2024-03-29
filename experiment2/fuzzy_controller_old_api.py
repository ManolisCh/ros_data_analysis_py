from docutils.nodes import rubric

import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt


input_error = 0.079

# crisp variables universe of discourse
crisp_error = np.arange(0, 0.101, 0.001)
crisp_output = np.arange(-1, 1.01, 0.01)

# fuzzy membership functions
fuzzy_error_small = fuzz.trapmf(crisp_error, [0, 0, 0.035, 0.06])
fuzzy_error_medium = fuzz.trapmf(crisp_error, [0.045, 0.06, 0.07, 0.085])
fuzzy_error_large = fuzz.trapmf(crisp_error, [0.07, 0.09, 0.1, 0.1])

fuzzy_output_change = fuzz.trimf(crisp_output, [0, 1, 1])
fuzzy_output_no_change = fuzz.trimf(crisp_output, [-1, -1, 0])


# Visualize these universes and membership functions
fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(8, 9))

ax0.plot(crisp_error, fuzzy_error_small, 'b', linewidth=1.5, label='small')
ax0.plot(crisp_error, fuzzy_error_medium, 'g', linewidth=1.5, label='medium')
ax0.plot(crisp_error, fuzzy_error_large, 'r', linewidth=1.5, label='large')
ax0.set_title('Error')
ax0.legend()
ax1.plot(crisp_output, fuzzy_output_no_change, 'b', linewidth=1.5, label='No change')
ax1.plot(crisp_output, fuzzy_output_change, 'g', linewidth=1.5, label='Maybe change')
ax1.set_title('Certainty of change')
ax1.legend()

# Turn off top/right axes
for ax in (ax0, ax1):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()


# find degree of the fuzzy membership functions of input(s)
error_level_small = fuzz.interp_membership(crisp_error, fuzzy_error_small, input_error)
error_level_medium = fuzz.interp_membership(crisp_error, fuzzy_error_medium, input_error)
error_level_large = fuzz.interp_membership(crisp_error, fuzzy_error_large, input_error)


print error_level_small
print error_level_medium
print error_level_large

# fuzzy rules

# rule 1, if error is small or medium then no change (disjunction as max)
active_rule1 = np.fmax(error_level_small, error_level_medium)
output_activation_no = np.fmin(active_rule1, fuzzy_output_no_change)

#rule 2, if error is large then change
output_activation_change = np.fmin(error_level_large, fuzzy_output_change)

output0 = np.zeros_like(crisp_output)

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.fill_between(crisp_output, output0, output_activation_no, facecolor='b', alpha=0.7)
ax0.plot(crisp_output, fuzzy_output_no_change, 'b', linewidth=0.5, linestyle='--', )
ax0.fill_between(crisp_output, output0, output_activation_change, facecolor='r', alpha=0.7)
ax0.plot(crisp_output, fuzzy_output_change, 'r', linewidth=0.5, linestyle='--')
ax0.set_title('Output membership activity')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

# Rule aggregation with max operator
aggregated = np.fmax(output_activation_no, output_activation_change)

# Defuzzification
output_decision = fuzz.defuzz(crisp_output, aggregated, 'mom')
output_activation = fuzz.interp_membership(crisp_output, aggregated, output_decision)  # for plot

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.plot(crisp_output, fuzzy_output_no_change, 'b', linewidth=0.5, linestyle='--', )
ax0.plot(crisp_output, fuzzy_output_change, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(crisp_output, output0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([output_decision, output_decision], [0, output_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Aggregated membership and result (line)')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

print output_decision
#plt.show()

