## EVALUATE AND PLOT maintenance_duration MODEL RESULTS

from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Evaluate model
def evaluate_models(models, X, y):
    predictions = np.mean([model.predict(X) for model in models], axis=0)
    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)
    return mse, r2

rf_mse, rf_r2 = evaluate_models(rf_models, X_test, y_test)

print("Random Forest Results:")
print(f"MSE: {rf_mse}, R2: {rf_r2}")

# Feature importance
feature_importance = rf_models[0].named_steps['feature_selection'].estimator_.feature_importances_
feature_names = (numeric_features_md + 
                 rf_models[0].named_steps['preprocessor']
                 .named_transformers_['cat']
                 .named_steps['onehot']
                 .get_feature_names_out(categorical_features_md).tolist())

# feature importances in descending order
indices = np.argsort(feature_importance)[::-1]

# feature ranking
print("\nFeature importance ranking:")
for f in range(min(20, len(feature_names))):
    print("%d. %s (%f)" % (f + 1, feature_names[indices[f]], feature_importance[indices[f]]))

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.title("Top 20 Feature Importances")
plt.bar(range(20), feature_importance[indices[:20]])
plt.xticks(range(20), [feature_names[i] for i in indices[:20]], rotation=90)
plt.tight_layout()
plt.show()

# actual vs predicted values
y_pred_rf = np.mean([model.predict(X_test) for model in rf_models], axis=0)
comparison_df_md = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred_rf
})

print("\nComparison of Actual vs Predicted maintenance_duration (Random Forest):")
print(comparison_df_md.head())

# Plot actual vs predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Maintenance Duration (Random Forest)')
plt.tight_layout()
plt.show()
