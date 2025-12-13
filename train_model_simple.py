# -*- coding: utf-8 -*-
"""Simple script to train the model"""
import os
import sys

# Fix encoding
if sys.platform == "win32":
    import codecs
    try:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    except:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crews.data_scientist_crew.tools import (
    LinearRegressionTrainer,
    RandomForestTrainer,
    GradientBoostingTrainer,
    ModelComparisonTool
)

def main():
    print("="*60)
    print("Training models...")
    print("="*60)
    
    features_path = "outputs/features.csv"
    if not os.path.exists(features_path):
        print(f"ERROR: Features file not found: {features_path}")
        return
    
    print(f"OK: Features file found")
    
    # Create trainers
    lr_trainer = LinearRegressionTrainer()
    rf_trainer = RandomForestTrainer()
    gb_trainer = GradientBoostingTrainer()
    comparison_tool = ModelComparisonTool()
    
    # Train models
    print("\nTraining Linear Regression...")
    lr_result = lr_trainer._run(features_path, "outputs")
    if 'error' in lr_result:
        print(f"ERROR: {lr_result['error']}")
        return
    print(f"OK: Linear Regression - Test RMSE: {lr_result['test_rmse']:.4f}, R^2: {lr_result['test_r2']:.4f}")
    
    print("\nTraining Random Forest...")
    rf_result = rf_trainer._run(features_path, "outputs")
    if 'error' in rf_result:
        print(f"ERROR: {rf_result['error']}")
        return
    print(f"OK: Random Forest - Test RMSE: {rf_result['test_rmse']:.4f}, R^2: {rf_result['test_r2']:.4f}")
    
    print("\nTraining Gradient Boosting...")
    gb_result = gb_trainer._run(features_path, "outputs")
    if 'error' in gb_result:
        print(f"ERROR: {gb_result['error']}")
        return
    print(f"OK: Gradient Boosting - Test RMSE: {gb_result['test_rmse']:.4f}, R^2: {gb_result['test_r2']:.4f}")
    
    # Compare and save
    print("\nComparing models and selecting best...")
    models_results = [lr_result, rf_result, gb_result]
    comparison_result = comparison_tool._run(models_results, "outputs")
    print(comparison_result)
    
    # Check results
    print("\n" + "="*60)
    if os.path.exists("outputs/model.pkl"):
        print("SUCCESS: Model saved to outputs/model.pkl")
    else:
        print("ERROR: Model not saved!")
    
    if os.path.exists("outputs/all_models_comparison.json"):
        print("SUCCESS: Model comparison saved")
    else:
        print("ERROR: Model comparison not saved!")
    print("="*60)

if __name__ == "__main__":
    main()

