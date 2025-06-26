from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectFromModel
from sklearn.decomposition import PCA

# Preprocessor
preprocessor_md = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('scaler', StandardScaler())
        ]), numeric_features_md),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ]), categorical_features_md)
    ])

# pipeline for RF
rf_pipeline = Pipeline([
    ('preprocessor', preprocessor_md),
    ('feature_selection', SelectFromModel(RandomForestRegressor(n_estimators=100, random_state=42))),
    ('pca', PCA(n_components=0.95)),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Hyperparameter tuning
param_distributions_rf = {
    'regressor__n_estimators': [50, 100, 200, 300, 400],
    'regressor__max_depth': [None, 10, 20, 30, 40, 50],
    'regressor__min_samples_split': [2, 5, 10, 15],
    'regressor__min_samples_leaf': [1, 2, 4, 6]
}

# Train models
rf_models = []

for sample in stratified_samples:
    X_train, X_test, y_train, y_test = train_test_split(sample, y_md.loc[sample.index], test_size=0.2, random_state=42)
    
    rf_search = RandomizedSearchCV(rf_pipeline, param_distributions_rf, n_iter=100, cv=3, scoring='r2', n_jobs=-1, random_state=42)
    rf_search.fit(X_train, y_train)
    rf_models.append(rf_search.best_estimator_)
