import skfuzzy as fuzz
import numpy as np

# fuzzy sets
crisp_error = fuzz.Antecedent(np.arange(0, 0.11, 0.01), 'error')
fuzzy_change = fuzz.Consequent(np.arange(0, 1.1, 0.1), 'change_control')

# fuzzy memberships
crisp_error['small'] = fuzz.trapmf(crisp_error.universe, [0, 0, 0.04, 0.06])
crisp_error['medium'] = fuzz.trapmf(crisp_error.universe, [0.04, 0.07, 0.08, 0.09])
crisp_error['large'] = fuzz.trapmf(crisp_error.universe, [0.08, 0.09, 0.1, 0.1])
fuzzy_change['no_change'] = fuzz.sigmf(fuzzy_change.universe, 0.8, -50)
fuzzy_change['change'] = fuzz.sigmf(fuzzy_change.universe, 0.8, 40)

# fuzzy rules
rule1 = fuzz.Rule(crisp_error['small'], fuzzy_change['no_change'])
rule2 = fuzz.Rule(crisp_error['medium'], fuzzy_change['no_changechange'])
rule3 = fuzz.Rule(crisp_error['large'], fuzzy_change['change'])

# controller
fuzzy_controller = fuzz.ControlSystem([rule1, rule2, rule3])

fuzzy_sim = fuzz.ControlSystemSimulation(fuzzy_controller)

fuzzy_sim.input['error'] = 0.7
fuzzy_sim.compute()
print fuzzy_sim.output


