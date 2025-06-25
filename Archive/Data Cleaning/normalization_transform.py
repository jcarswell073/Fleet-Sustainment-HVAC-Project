import numpy as np
from scipy.stats import boxcox




# Normalize price/costs
hvacdata['total_price_log'] = np.log(hvacdata['total_price'] + 1)
hvacdata['days_open_boxcox'], _ = boxcox(hvacdata['days_open'] + 1)
hvacdata['total_material_cost_log'] = np.log(hvacdata['total_material_cost'] + 1)
hvacdata['total_repair_replacement_cost_log'] = np.log(hvacdata['total_repair_replacement_cost'] + 1)
merged1['total_ship_force_man_hours_boxcox'], _ = boxcox(merged1['total_ship_force_man_hours'] + 1)  # Adding 1 to handle zero values



# Plot histograms
plt.hist(hvacdata['total_price_log'], bins=10, edgecolor='black')
plt.title('Histogram of total_price_log')
plt.show()

