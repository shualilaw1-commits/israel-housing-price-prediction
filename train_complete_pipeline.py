"""
סקריפט מלא לאימון המודל על נתוני ישראל
מריץ את כל השלבים: טעינה -> ניקוי -> פיצ'רים -> אימון
"""
import os
import sys

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

from crews.data_analyst_crew.tools import DataIngestionTool, DataCleaningTool
from crews.data_scientist_crew.tools import (
    FeatureEngineeringTool,
    LinearRegressionTrainer,
    RandomForestTrainer,
    GradientBoostingTrainer,
    ModelComparisonTool
)

def main():
    print("="*60)
    print("Pipeline מלא לאימון מודל על נתוני ישראל")
    print("="*60)

    output_dir = "outputs"

    # שלב 1: טעינת נתונים
    print("\n[שלב 1/5] טעינת נתונים...")
    print("-"*60)
    ingestion_tool = DataIngestionTool()
    result = ingestion_tool._run(output_dir)
    print(result)
    if "שגיאה" in result or "ERROR" in result or "לא נמצא" in result:
        print("\nERROR: הטעינה נכשלה. אנא הרץ תחילה: python create_israel_dataset.py")
        return

    # שלב 2: ניקוי נתונים
    print("\n[שלב 2/5] ניקוי נתונים...")
    print("-"*60)
    cleaning_tool = DataCleaningTool()
    result = cleaning_tool._run("outputs/raw_data.csv", output_dir)
    print(result)
    if "שגיאה" in result or "ERROR" in result:
        print("\nERROR: הניקוי נכשל")
        return

    # שלב 3: יצירת פיצ'רים
    print("\n[שלב 3/5] יצירת פיצ'רים...")
    print("-"*60)
    feature_tool = FeatureEngineeringTool()
    result = feature_tool._run("outputs/clean_data.csv", output_dir)
    print(result)
    if "שגיאה" in result or "ERROR" in result:
        print("\nERROR: יצירת הפיצ'רים נכשלה")
        return

    # בדיקה שקובץ הפיצ'רים נוצר
    features_path = "outputs/features.csv"
    if not os.path.exists(features_path):
        print(f"\nERROR: קובץ הפיצ'רים לא נמצא: {features_path}")
        return

    print(f"\n[OK] קובץ הפיצ'רים נוצר: {features_path}")

    # שלב 4: אימון מודלים
    print("\n[שלב 4/5] אימון מודלים...")
    print("="*60)

    lr_trainer = LinearRegressionTrainer()
    rf_trainer = RandomForestTrainer()
    gb_trainer = GradientBoostingTrainer()

    print("\n[4.1] מאמן Linear Regression...")
    print("-"*60)
    lr_result = lr_trainer._run(features_path, output_dir)
    if 'error' in lr_result:
        print(f"ERROR: {lr_result['error']}")
        return
    print(f"[OK] Linear Regression - Test RMSE: {lr_result['test_rmse']:.4f}, R^2: {lr_result['test_r2']:.4f}")

    print("\n[4.2] מאמן Random Forest...")
    print("-"*60)
    rf_result = rf_trainer._run(features_path, output_dir)
    if 'error' in rf_result:
        print(f"ERROR: {rf_result['error']}")
        return
    print(f"[OK] Random Forest - Test RMSE: {rf_result['test_rmse']:.4f}, R^2: {rf_result['test_r2']:.4f}")

    print("\n[4.3] מאמן Gradient Boosting...")
    print("-"*60)
    gb_result = gb_trainer._run(features_path, output_dir)
    if 'error' in gb_result:
        print(f"ERROR: {gb_result['error']}")
        return
    print(f"[OK] Gradient Boosting - Test RMSE: {gb_result['test_rmse']:.4f}, R^2: {gb_result['test_r2']:.4f}")

    # שלב 5: השוואת מודלים
    print("\n[שלב 5/5] השוואת מודלים ובחירת הטוב ביותר...")
    print("="*60)
    comparison_tool = ModelComparisonTool()
    models_results = [lr_result, rf_result, gb_result]
    comparison_result = comparison_tool._run(models_results, output_dir)
    print(comparison_result)

    # בדיקת קבצי פלט
    print("\n" + "="*60)
    print("בדיקת קבצי פלט:")
    print("="*60)

    files_to_check = [
        ("model.pkl", "המודל הטוב ביותר"),
        ("all_models_comparison.json", "השוואת מודלים"),
        ("features.csv", "קובץ פיצ'רים"),
        ("clean_data.csv", "נתונים מנוקים"),
    ]

    all_ok = True
    for filename, description in files_to_check:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            print(f"[OK] {description}: {filepath}")
        else:
            print(f"[ERROR] {description} לא נמצא: {filepath}")
            all_ok = False

    print("\n" + "="*60)
    if all_ok:
        print("SUCCESS! האימון הושלם בהצלחה!")
        print("="*60)
        print("\nעכשיו תוכל להריץ את ה-Dashboard:")
        print("  streamlit run app/streamlit_app.py")
    else:
        print("WARNING: האימון הושלם אך חלק מהקבצים חסרים")
        print("="*60)

if __name__ == "__main__":
    main()
