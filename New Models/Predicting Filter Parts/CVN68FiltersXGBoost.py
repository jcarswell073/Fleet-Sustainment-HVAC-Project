import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.model_selection import RandomizedSearchCV

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








##----------------XGBoost Model----------------##

part = 'FILTER ELEMENT,AIR'
ship = 'CVN68'

df_xgb = monthly_part_summary[
    (monthly_part_summary['niin_nomenclature'] == part) &
    (monthly_part_summary['ship'] == ship)
].copy()

df_xgb['calendar_month'] = df_xgb['calendar_month'].dt.to_timestamp()
df_xgb['month'] = df_xgb['calendar_month'].dt.month
df_xgb['year'] = df_xgb['calendar_month'].dt.year
df_xgb['quantity_lag1'] = df_xgb['total_part_quantity'].shift(1)

# extra features
extra_features_xgb = (
    hvacdata.groupby(['ship', 'calendar_month', 'niin_nomenclature'])
    .agg(
        avg_maintenance_duration=('maintenance_duration', 'mean'),
        total_ship_force_man_hours_sum=('total_ship_force_man_hours', 'sum'),
        avg_days_open=('days_open', 'mean'),
        component_status_mode=('component_status', lambda x: x.mode().iloc[0] if not x.mode().empty else None),
        def_narrative_filter_related=('def_narrative_filter_related', 'sum'),
        def_narrative_maintenance_related=('def_narrative_maintenance_related', 'sum'),
        def_narrative_replacement_related=('def_narrative_replacement_related', 'sum'),
    )
    .reset_index()
)

df_xgb = df_xgb.merge(extra_features_xgb, on=['ship', 'calendar_month', 'niin_nomenclature'], how='left')
df_xgb = df_xgb.dropna()

# features
X_xgb = df_xgb[[
    'month', 'year', 'num_jobs', 'quantity_lag1',
    'avg_maintenance_duration', 'total_ship_force_man_hours_sum',
    'avg_days_open', 'def_narrative_filter_related',
    'component_status_mode',
    'def_narrative_replacement_related'
]]

X_xgb = pd.get_dummies(X_xgb, columns=['component_status_mode'], drop_first=True)
y_xgb = df_xgb['total_part_quantity']

# split
train_size_xgb = int(len(df_xgb) - 5)
X_train_xgb, X_test_xgb = X_xgb.iloc[:train_size_xgb], X_xgb.iloc[train_size_xgb:]
y_train_xgb, y_test_xgb = y_xgb.iloc[:train_size_xgb], y_xgb.iloc[train_size_xgb:]


# hyperparameter tuning
param_dist = {
    'n_estimators': [200, 300, 500],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 4, 5],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0]
}

xgb_for_search = XGBRegressor(random_state=42)

random_search = RandomizedSearchCV(
    estimator=xgb_for_search,
    param_distributions=param_dist,
    n_iter=20,
    scoring='neg_mean_squared_error',
    cv=3,
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train_xgb, y_train_xgb)

print("\nBest Parameters Found:", random_search.best_params_)



# model
xgb_model = random_search.best_estimator_

# predict
y_pred_xgb = xgb_model.predict(X_test_xgb)

mse_xgb = mean_squared_error(y_test_xgb, y_pred_xgb)
print(f"\nTuned XGBoost Test MSE: {mse_xgb:.2f}")

results_xgb = pd.DataFrame({
    'calendar_month': df_xgb['calendar_month'].iloc[train_size_xgb:].astype(str),
    'actual': y_test_xgb,
    'predicted': y_pred_xgb
})
print(results_xgb)



# feature importance
xgb_importance_df = pd.DataFrame({
    'feature': X_train_xgb.columns,
    'importance': xgb_model.feature_importances_
}).sort_values(by='importance', ascending=False)

print("\nXGBoost Feature Importances:")
print(xgb_importance_df)

# plot
plt.figure(figsize=(10, 6))
plt.barh(xgb_importance_df['feature'], xgb_importance_df['importance'])
plt.xlabel("Importance")
plt.title("XGBoost Feature Importance")
plt.gca().invert_yaxis()
plt.show()

