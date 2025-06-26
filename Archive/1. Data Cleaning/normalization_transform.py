import numpy as np
from scipy.stats import boxcox




hvacdata['total_price_log'] = np.log(hvacdata['total_price'] + 1)
hvacdata['days_open_boxcox'], _ = boxcox(hvacdata['days_open'] + 1)
hvacdata['total_material_cost_log'] = np.log(hvacdata['total_material_cost'] + 1)
hvacdata['total_repair_replacement_cost_log'] = np.log(hvacdata['total_repair_replacement_cost'] + 1)
hvacdata['total_ship_force_man_hours_boxcox'], _ = boxcox(hvacdata['total_ship_force_man_hours'] + 1)
hvacdata['maintenance_duration_log'] = np.log(hvacdata['maintenance_duration'] + 1)


