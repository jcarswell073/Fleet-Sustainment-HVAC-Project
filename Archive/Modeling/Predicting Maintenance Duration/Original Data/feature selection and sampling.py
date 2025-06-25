import numpy as np
import pandas as pd

# target and features
target_md = 'maintenance_duration'
features_md = [
    'eswbs_opening', 'type_availability_code', 'deferral_reason',
    'total_ima_man_hours', 'total_ship_force_man_hours_boxcox',
    'total_material_cost_log', 'def_narrative_fan_related', 'action_taken_code', 'when_discovered',
    'def_narrative_filter_related', 'def_narrative_coil_related', 'def_narrative_replacement_related'
]

X_md = hvacdata[features_md]
y_md = hvacdata[target_md]

# numeric and categorical features
numeric_features_md = [
    'total_ima_man_hours', 'total_ship_force_man_hours_boxcox',
    'total_material_cost_log'
]

categorical_features_md = [
    'eswbs_opening', 'type_availability_code', 'deferral_reason',
    'def_narrative_fan_related', 'action_taken_code', 'when_discovered',
    'def_narrative_filter_related', 'def_narrative_coil_related', 'def_narrative_replacement_related'
]

# Ensure categorical columns are treated correctly
X_md[categorical_features_md] = X_md[categorical_features_md].astype(str)

# Stratified sampling by type_of_maintenance_action
from sklearn.model_selection import StratifiedKFold

n_splits = 5
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
stratified_samples = []

for train_index, _ in skf.split(X_md, hvacdata["type_of_maintenance_action"]):
    stratified_samples.append(X_md.iloc[train_index])
