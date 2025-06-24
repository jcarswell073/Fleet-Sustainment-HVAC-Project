import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import RFE

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

# Ensure categorical columns are treated correctly
X_pms[categorical_features] = X_pms[categorical_features].astype(str)

# Preprocessor with polynomial features for numeric data and one-hot encoding for categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ]), categorical_features)
    ])

# Split data
X_train_pms, X_test_pms, y_train_pms, y_test_pms = train_test_split(X_pms, y_pms, test_size=0.2, random_state=42)

# Fit and transform training data
X_train_processed_pms = preprocessor.fit_transform(X_train_pms)

# Transform test data
X_test_processed_pms = preprocessor.transform(X_test_pms)

# Feature selection using RFE
rf_estimator = RandomForestRegressor(n_estimators=100, random_state=42)
selector = RFE(estimator=rf_estimator, n_features_to_select=20)
X_train_selected_pms = selector.fit_transform(X_train_processed_pms, y_train_pms)
X_test_selected_pms = selector.transform(X_test_processed_pms)

# Train model with hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}
grid_search = GridSearchCV(estimator=rf_estimator, param_grid=param_grid, cv=5, scoring='r2', n_jobs=-1)
grid_search.fit(X_train_selected_pms, y_train_pms)

# Best model
best_rf_model_pms = grid_search.best_estimator_

# Predict
y_pred_pms = best_rf_model_pms.predict(X_test_selected_pms)

# Evaluate model
mse_pms = mean_squared_error(y_test_pms, y_pred_pms)
r2_pms = r2_score(y_test_pms, y_pred_pms)

print(f"PMS-related Mean Squared Error: {mse_pms}")
print(f"PMS-related R-squared Score: {r2_pms}")

# Retrieve names of all features
numeric_feature_names = preprocessor.named_transformers_['num']['poly'].get_feature_names_out(numeric_features)
categorical_feature_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)

all_feature_names = list(numeric_feature_names) + list(categorical_feature_names)

# Plot feature importances
selected_feature_names = [all_feature_names[i] for i in range(len(all_feature_names)) if selector.support_[i]]

feature_importance_pms = pd.DataFrame({
    'feature': selected_feature_names,
    'importance': best_rf_model_pms.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x='importance', y='feature', data=feature_importance_pms.head(20))
plt.title('Top 20 Most Important Features')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()

print("\nAll Feature Importances:")
print(feature_importance_pms.to_string(index=False))

# Create the comparison dataframe with log values
comparison_df = pd.DataFrame({
    'Actual': y_test_pms,
    'Predicted': y_pred_pms
})

# Add columns with non-log (original scale) values
comparison_df['Actual_Original'] = np.exp(comparison_df['Actual'])
comparison_df['Predicted_Original'] = np.exp(comparison_df['Predicted'])

# Reorder columns to show original scale values first
comparison_df = comparison_df[['Actual_Original', 'Predicted_Original', 'Actual', 'Predicted']]

# Display the first 15 rows
print(comparison_df.head(15))
