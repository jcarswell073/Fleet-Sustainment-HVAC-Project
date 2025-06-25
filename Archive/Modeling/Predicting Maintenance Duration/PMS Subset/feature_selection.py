

from scipy.stats import boxcox



hvacdata['date_closing'] = pd.to_datetime(hvacdata['date_closing'], errors='coerce')
hvacdata['date_maintenance_action'] = pd.to_datetime(hvacdata['date_maintenance_action'], errors='coerce')



hvacdata['maintenance_duration'] = (
    pd.to_datetime(hvacdata['date_closing']) - pd.to_datetime(hvacdata['date_maintenance_action'])
).dt.days



hvacdata['maintenance_duration'] = (hvacdata['date_closing'] - hvacdata['date_maintenance_action']).dt.days


# Normalize price/costs
hvacdata['total_price_log'] = np.log(hvacdata['total_price'] + 1)
hvacdata['days_open_boxcox'], _ = boxcox(hvacdata['days_open'] + 1)
hvacdata['total_material_cost_log'] = np.log(hvacdata['total_material_cost'] + 1)
hvacdata['total_repair_replacement_cost_log'] = np.log(hvacdata['total_repair_replacement_cost'] + 1)
hvacdata['total_ship_force_man_hours_boxcox'], _ = boxcox(hvacdata['total_ship_force_man_hours'] + 1)
hvacdata['maintenance_duration_log'] = np.log(hvacdata['maintenance_duration'] + 1)


# Subset data for 'PMS'
pms_related = subset_data_by_keyword(hvacdata, 'PMS', narrative_columns)


# target and features
target = 'maintenance_duration_log'
selected_features = [
    'eswbs_opening', 'type_availability_code', 'deferral_reason',
    'total_ima_man_hours', 'total_ship_force_man_hours_boxcox',
    'total_material_cost_log', 'def_narrative_fan_related', 'action_taken_code', 'when_discovered',
    'def_narrative_filter_related', 'def_narrative_coil_related', 'def_narrative_replacement_related'
]

X_pms = pms_related[selected_features]
y_pms = pms_related[target]

# Define numeric and categorical
numeric_features = [
    'total_ima_man_hours', 'total_ship_force_man_hours_boxcox',
    'total_material_cost_log'
]

categorical_features = [
    'eswbs_opening', 'type_availability_code', 'deferral_reason',
    'def_narrative_fan_related', 'action_taken_code', 'when_discovered',
    'def_narrative_filter_related', 'def_narrative_coil_related', 'def_narrative_replacement_related'
]
