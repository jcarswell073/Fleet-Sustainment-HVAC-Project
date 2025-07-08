import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

hvacdata = pd.read_csv('Archive/2. ProcessedData/dataset.csv')


# feature engineering maintenance duration

hvacdata['date_closing'] = pd.to_datetime(hvacdata['date_closing'], errors='coerce')
hvacdata['date_maintenance_action'] = pd.to_datetime(hvacdata['date_maintenance_action'], errors='coerce')

hvacdata = hvacdata.dropna(subset=['date_closing', 'date_maintenance_action'])


hvacdata['maintenance_duration'] = (
    hvacdata['date_closing'] - hvacdata['date_maintenance_action']
).dt.days

# drop negatives
hvacdata.loc[hvacdata['maintenance_duration'] < 0, 'maintenance_duration'] = pd.NA
hvacdata = hvacdata.dropna(subset=['maintenance_duration'])


hvacdata['date_maintenance_action'] = pd.to_datetime(hvacdata['date_maintenance_action'], errors='coerce')
hvacdata['calendar_month'] = hvacdata['date_maintenance_action'].dt.to_period('M')



# groups data by ship, months_since_rcoh_start, and part

monthly_part_summary = (
    hvacdata.groupby(['ship', 'calendar_month', 'niin_nomenclature'])
    .agg(
        total_part_quantity=('quantity', 'sum'),
        num_jobs=('job_status', 'count'),
    )
    .reset_index()
)




# text engineering (preprocess)

def_narrative_patterns = {
    'maintenance_related': r'\bmaintenance|pm|preventive maintenance|inspection|check|routine\b',
    'repair_related': r'\brepair|troubleshoot|fix|correct\b',
    'replacement_related': r'\breplace|new|install|procure\b',
    'cleaning_related': r'\bclean|vacuum|wash\b',
    'corrosion_related': r'\bcorrosion|rust|preserve\b',
    'fan_related': r'\bfan\b',
    'coil_related': r'\bcoil\b',
    'filter_related': r'\bfilter\b',
    'motor_related': r'\bmotor\b',
    'valve_related': r'\bvalve\b',
    'switch_related': r'\bswitch\b',
    'belt_related': r'\bbelt\b'
}

def create_binary_features(df, column, patterns):
    features = {}
    for key, pattern in patterns.items():
        features[f'{column}_{key}'] = df[column].astype(str).str.contains(pattern, case=False, regex=True, na=False).astype(int)
    return pd.DataFrame(features)
    

def_narrative_features = create_binary_features(hvacdata, 'def_narrative', def_narrative_patterns)

hvacdata = pd.concat([hvacdata, def_narrative_features], axis=1)

hvacdata['calendar_month'] = hvacdata['date_maintenance_action'].dt.to_period('M').dt.to_timestamp()



##---------------MODEL---------------##
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# monthly_part_summary: ship, niin_nomenclature, calendar_month, total_part_quantity, num_jobs, total_material_cost

part = 'FILTER ELEMENT,AIR'
ship = 'CVN68'

df = monthly_part_summary[
    (monthly_part_summary['niin_nomenclature'] == part) &
    (monthly_part_summary['ship'] == ship)
].copy()


df['calendar_month'] = df['calendar_month'].dt.to_timestamp()
df['month'] = df['calendar_month'].dt.month
df['year'] = df['calendar_month'].dt.year

# lag features that helps model learn from prior months
# e.g. if last month was high, maybe next month will be high  as well
df['quantity_lag1'] = df['total_part_quantity'].shift(1)



# extra features
extra_features = (
    hvacdata.groupby(['ship', 'calendar_month', 'niin_nomenclature'])
    .agg(
        avg_maintenance_duration=('maintenance_duration', 'mean'),
        total_ima_man_hours_sum=('total_ima_man_hours', 'sum'),
        total_ship_force_man_hours_sum=('total_ship_force_man_hours', 'sum'),
        avg_days_open=('days_open', 'mean'),
        type_availability_code_mode=('type_availability_code', lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        component_status_mode=('component_status', lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        type_of_maintenance_action_mode=('type_of_maintenance_action', lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        type_of_availability_needed_mode=('type_of_availability_needed', lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        def_narrative_filter_related=('def_narrative_filter_related', 'sum'),
        def_narrative_maintenance_related=('def_narrative_maintenance_related', 'sum'),
        def_narrative_replacement_related=('def_narrative_replacement_related', 'sum')
    )
    .reset_index()
)



# merging extra features to df
df = df.merge(
    extra_features,
    on=['ship', 'calendar_month', 'niin_nomenclature'],
    how='left'
)

df = df.dropna()



# feature selection
X = df[[
    'month', 'year', 'num_jobs', 'avg_maintenance_duration',
    'total_ship_force_man_hours_sum', 'avg_days_open',
    'def_narrative_filter_related', 'def_narrative_maintenance_related',
    'component_status_mode',
    'def_narrative_replacement_related'
]]

# One-hot encode
X = pd.get_dummies(X, columns=['component_status_mode',], drop_first=True)

y = df['total_part_quantity']

# (last 5 months as test)
train_size = int(len(df) - 5)
X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

# model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"Test MSE: {mse:.2f}")

results = pd.DataFrame({
    'calendar_month': df['calendar_month'].iloc[train_size:].astype(str),
    'actual': y_test,
    'predicted': y_pred
})
print(results)











