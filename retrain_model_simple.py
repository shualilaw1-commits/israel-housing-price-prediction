# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("Retraining Model - Israel Housing (No Lat/Lon)")
print("=" * 60)

# Load data
print("\nLoading data...")
df = pd.read_csv('outputs/features.csv')

# Prepare features and target
X = df.drop('Price_Millions', axis=1)
y = df['Price_Millions']

print(f"Data: {len(df)} rows, {len(X.columns)} features")
print(f"Features: {list(X.columns)}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Gradient Boosting (best performer from previous analysis)
print("\nTraining Gradient Boosting model...")
param_grid = {
    'n_estimators': [200],
    'learning_rate': [0.1],
    'max_depth': [3],
    'min_samples_split': [2]
}

gb = GradientBoostingRegressor(random_state=42)
grid_search = GridSearchCV(gb, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Evaluate
train_pred = best_model.predict(X_train)
test_pred = best_model.predict(X_test)

train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
test_r2 = r2_score(y_test, test_pred)

print(f"\nResults:")
print(f"Train RMSE: {train_rmse:.4f}")
print(f"Test RMSE: {test_rmse:.4f}")
print(f"Test R2: {test_r2:.4f}")
print(f"Best params: {grid_search.best_params_}")

# Save model
model_data = {
    'model': best_model,
    'scaler': None,
    'model_name': 'Gradient Boosting',
    'metrics': {
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'test_r2': test_r2
    },
    'features': list(X.columns)
}

joblib.dump(model_data, 'outputs/model.pkl')
print("\nModel saved to: outputs/model.pkl")
print(f"Features used: {len(X.columns)}")
print("=" * 60)
