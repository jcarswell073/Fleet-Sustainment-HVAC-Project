# Normalize price/costs
merged['total_price_log'] = np.log(merged['total_price'] + 1)
merged['days_open_boxcox'], _ = boxcox(merged['days_open'] + 1)
merged['total_material_cost_log'] = np.log(merged['total_material_cost'] + 1)
merged['total_repair_replacement_cost_log'] = np.log(merged['total_repair_replacement_cost'] + 1)


# Plot histograms
plt.hist(merged['total_price_log'], bins=10, edgecolor='black')
plt.title('Histogram of total_price_log')
plt.show()

