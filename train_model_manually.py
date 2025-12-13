"""
סקריפט לאימון המודל ידנית - במקרה שה-Agent לא הצליח
"""
import os
import sys
import json
import joblib

# Fix encoding for Windows
if sys.platform == "win32":
    import codecs
    try:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    except (AttributeError, ValueError):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# הוספת נתיב הפרויקט
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crews.data_scientist_crew.tools import (
    LinearRegressionTrainer,
    RandomForestTrainer,
    GradientBoostingTrainer,
    ModelComparisonTool
)

def main():
    print("="*60)
    print("מתחיל אימון מודלים ידנית")
    print("="*60)
    
    # בדיקה שקובץ הפיצ'רים קיים
    features_path = "outputs/features.csv"
    if not os.path.exists(features_path):
        print(f"ERROR: קובץ הפיצ'רים לא נמצא: {features_path}")
        return
    
    print(f"\nOK: קובץ הפיצ'רים נמצא: {features_path}")
    
    # יצירת כלי האימון
    lr_trainer = LinearRegressionTrainer()
    rf_trainer = RandomForestTrainer()
    gb_trainer = GradientBoostingTrainer()
    comparison_tool = ModelComparisonTool()
    
    # אימון כל המודלים
    print("\n" + "="*60)
    print("מאמן Linear Regression...")
    print("="*60)
    lr_result = lr_trainer._run(features_path, "outputs")
    if 'error' in lr_result:
        print(f"ERROR: {lr_result['error']}")
        return
    print(f"OK: Linear Regression - Test RMSE: {lr_result['test_rmse']:.4f}, R^2: {lr_result['test_r2']:.4f}")
    
    print("\n" + "="*60)
    print("מאמן Random Forest...")
    print("="*60)
    rf_result = rf_trainer._run(features_path, "outputs")
    if 'error' in rf_result:
        print(f"ERROR: {rf_result['error']}")
        return
    print(f"OK: Random Forest - Test RMSE: {rf_result['test_rmse']:.4f}, R^2: {rf_result['test_r2']:.4f}")
    
    print("\n" + "="*60)
    print("מאמן Gradient Boosting...")
    print("="*60)
    gb_result = gb_trainer._run(features_path, "outputs")
    if 'error' in gb_result:
        print(f"ERROR: {gb_result['error']}")
        return
    print(f"OK: Gradient Boosting - Test RMSE: {gb_result['test_rmse']:.4f}, R^2: {gb_result['test_r2']:.4f}")
    
    # השוואת מודלים ושמירה
    print("\n" + "="*60)
    print("משווה מודלים ובוחר את הטוב ביותר...")
    print("="*60)
    models_results = [lr_result, rf_result, gb_result]
    comparison_result = comparison_tool._run(models_results, "outputs")
    print(comparison_result)
    
    # בדיקה שהמודל נשמר
    if os.path.exists("outputs/model.pkl"):
        print("\nSUCCESS: המודל נשמר בהצלחה ב: outputs/model.pkl")
    else:
        print("\nERROR: המודל לא נשמר!")
    
    if os.path.exists("outputs/all_models_comparison.json"):
        print("SUCCESS: השוואת מודלים נשמרה ב: outputs/all_models_comparison.json")
    else:
        print("ERROR: השוואת מודלים לא נשמרה!")
    
    print("\n" + "="*60)
    print("אימון המודלים הושלם!")
    print("="*60)

if __name__ == "__main__":
    main()

