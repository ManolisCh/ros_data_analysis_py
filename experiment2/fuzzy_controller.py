from docutils.nodes import rubric

import skfuzzy as fuzz
import numpy as np

# fuzzy sets
crisp_error = fuzz.Antecedent(np.arange(0, 0.11, 0.01), 'error')
fuzzy_change = fuzz.Consequent(np.arange(-1, 1.1, 0.1), 'change_control')

# fuzzy memberships
crisp_error['small'] = fuzz.trapmf(crisp_error.universe, [0, 0, 0.035, 0.06])
crisp_error['medium'] = fuzz.trapmf(crisp_error.universe, [0.045, 0.06, 0.07, 0.085])
crisp_error['large'] = fuzz.trapmf(crisp_error.universe, [0.07, 0.09, 0.1, 0.1])
fuzzy_change['no_change'] = fuzz.trimf(fuzzy_change.universe, [-1, -1, 0])
fuzzy_change['change'] = fuzz.trimf(fuzzy_change.universe, [0, 1, 1])

# fuzzy rules
rule1 = fuzz.Rule(crisp_error['small'], fuzzy_change['no_change'])
rule2 = fuzz.Rule(crisp_error['medium'], fuzzy_change['no_change'])
rule3 = fuzz.Rule(crisp_error['large'], fuzzy_change['change'])
# controller
fuzzy_controller = fuzz.ControlSystem([rule1, rule2, rule3])

fuzzy_sim = fuzz.ControlSystemSimulation(fuzzy_controller)

fuzzy_sim.input['error'] = 0.01
fuzzy_sim.compute()
print fuzzy_sim.output


