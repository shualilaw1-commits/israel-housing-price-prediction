# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("Advanced Model Analysis - Israel Housing")
print("=" * 60)

# Load data
print("\n[1/6] Loading data and model...")
df = pd.read_csv('outputs/features.csv')
model_data = joblib.load('outputs/model.pkl')

X = df.drop('Price_Millions', axis=1)
y = df['Price_Millions']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

current_model = model_data['model']
print(f"Data: {len(df)} rows, {len(X.columns)} features")
print(f"Model: {model_data['model_name']}")

# Overfitting check
print("\n[2/6] Overfitting Analysis...")
print("-" * 60)

train_pred = current_model.predict(X_train)
test_pred = current_model.predict(X_test)

train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
train_r2 = r2_score(y_train, train_pred)
test_r2 = r2_score(y_test, test_pred)

gap = test_rmse - train_rmse
gap_pct = (gap / train_rmse) * 100

print(f"\nTrain RMSE: {train_rmse:.4f} | R2: {train_r2:.4f}")
print(f"Test RMSE:  {test_rmse:.4f} | R2: {test_r2:.4f}")
print(f"Gap: {gap:.4f} ({gap_pct:.2f}%)")

if gap_pct < 10:
    print("Status: Good - No significant overfitting")
elif gap_pct < 20:
    print("Status: Warning - Slight overfitting")
else:
    print("Status: Problem - Significant overfitting")

# Feature Importance
print("\n[3/6] Feature Importance Analysis...")
print("-" * 60)

if hasattr(current_model, 'feature_importances_'):
    importances = current_model.feature_importances_
    feat_imp = pd.DataFrame({
        'feature': X.columns,
        'importance': importances
    }).sort_values('importance', ascending=False)

    print("\nTop 10 Important Features:")
    for idx, row in feat_imp.head(10).iterrows():
        print(f"  {row['feature']:30s} {row['importance']:.4f}")

    # Save plot
    plt.figure(figsize=(12, 8))
    top15 = feat_imp.head(15)
    plt.barh(range(len(top15)), top15['importance'])
    plt.yticks(range(len(top15)), top15['feature'])
    plt.xlabel('Importance')
    plt.title('Top 15 Feature Importance')
    plt.tight_layout()
    plt.savefig('outputs/feature_importance.png', dpi=300)
    print("\nSaved: outputs/feature_importance.png")

# Hyperparameter Tuning - Random Forest
print("\n[4/6] Tuning Random Forest...")
print("-" * 60)

param_grid_rf = {
    'n_estimators': [200, 300],
    'max_depth': [10, 15, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

rf_tuned = RandomForestRegressor(random_state=42, n_jobs=-1)
grid_rf = GridSearchCV(rf_tuned, param_grid_rf, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1, verbose=0)
grid_rf.fit(X_train, y_train)

print(f"\nBest params: {grid_rf.best_params_}")
rf_best = grid_rf.best_estimator_
rf_pred = rf_best.predict(X_test)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_r2 = r2_score(y_test, rf_pred)

print(f"Test RMSE: {rf_rmse:.4f} | R2: {rf_r2:.4f}")
print(f"Improvement: {((test_rmse - rf_rmse) / test_rmse * 100):.2f}%")

# Hyperparameter Tuning - Gradient Boosting
print("\n[5/6] Tuning Gradient Boosting...")
print("-" * 60)

param_grid_gb = {
    'n_estimators': [200, 300],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5]
}

gb_tuned = GradientBoostingRegressor(random_state=42)
grid_gb = GridSearchCV(gb_tuned, param_grid_gb, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1, verbose=0)
grid_gb.fit(X_train, y_train)

print(f"\nBest params: {grid_gb.best_params_}")
gb_best = grid_gb.best_estimator_
gb_pred = gb_best.predict(X_test)
gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
gb_r2 = r2_score(y_test, gb_pred)

print(f"Test RMSE: {gb_rmse:.4f} | R2: {gb_r2:.4f}")
print(f"Improvement: {((test_rmse - gb_rmse) / test_rmse * 100):.2f}%")

# Final Comparison
print("\n[6/6] Final Model Comparison...")
print("=" * 60)

comparison = pd.DataFrame({
    'Model': ['Original', 'RF Tuned', 'GB Tuned'],
    'RMSE': [test_rmse, rf_rmse, gb_rmse],
    'R2': [test_r2, rf_r2, gb_r2]
}).sort_values('RMSE')

print("\n" + comparison.to_string(index=False))

best_idx = comparison.iloc[0]
print(f"\nBest Model: {best_idx['Model']}")
print(f"RMSE: {best_idx['RMSE']:.4f}")
print(f"R2: {best_idx['R2']:.4f}")

# Save best model
if best_idx['Model'] == 'RF Tuned':
    best_model = rf_best
elif best_idx['Model'] == 'GB Tuned':
    best_model = gb_best
else:
    best_model = current_model

improved_data = {
    'model': best_model,
    'scaler': model_data.get('scaler'),
    'model_name': best_idx['Model'],
    'metrics': {
        'train_rmse': np.sqrt(mean_squared_error(y_train, best_model.predict(X_train))),
        'test_rmse': best_idx['RMSE'],
        'test_r2': best_idx['R2']
    }
}

joblib.dump(improved_data, 'outputs/model_improved.pkl')
print("\nSaved: outputs/model_improved.pkl")

# Visualizations
print("\nCreating visualizations...")
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Predicted vs Actual
axes[0, 0].scatter(y_test, test_pred, alpha=0.5, label='Original')
axes[0, 0].scatter(y_test, rf_pred, alpha=0.5, label='RF Tuned')
axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0, 0].set_xlabel('Actual Price')
axes[0, 0].set_ylabel('Predicted Price')
axes[0, 0].set_title('Predicted vs Actual')
axes[0, 0].legend()

# Residuals
res_orig = y_test - test_pred
res_rf = y_test - rf_pred
axes[0, 1].scatter(test_pred, res_orig, alpha=0.5, label='Original')
axes[0, 1].scatter(rf_pred, res_rf, alpha=0.5, label='RF Tuned')
axes[0, 1].axhline(y=0, color='r', linestyle='--')
axes[0, 1].set_xlabel('Predicted')
axes[0, 1].set_ylabel('Residuals')
axes[0, 1].set_title('Residual Plot')
axes[0, 1].legend()

# Error Distribution
axes[1, 0].hist(res_orig, bins=50, alpha=0.5, label='Original')
axes[1, 0].hist(res_rf, bins=50, alpha=0.5, label='RF Tuned')
axes[1, 0].set_xlabel('Residuals')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Residual Distribution')
axes[1, 0].legend()

# RMSE Comparison
models = ['Original', 'RF Tuned', 'GB Tuned']
rmses = [test_rmse, rf_rmse, gb_rmse]
axes[1, 1].barh(models, rmses, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[1, 1].set_xlabel('Test RMSE')
axes[1, 1].set_title('RMSE Comparison')
for i, v in enumerate(rmses):
    axes[1, 1].text(v, i, f' {v:.4f}', va='center')

plt.tight_layout()
plt.savefig('outputs/advanced_analysis.png', dpi=300)
print("Saved: outputs/advanced_analysis.png")

print("\n" + "=" * 60)
print("Analysis Complete!")
print("=" * 60)
print("\nOutput files:")
print("  - outputs/feature_importance.png")
print("  - outputs/advanced_analysis.png")
print("  - outputs/model_improved.pkl")
