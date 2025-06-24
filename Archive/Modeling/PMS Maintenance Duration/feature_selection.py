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
