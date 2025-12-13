"""
סקריפט ליצירת evaluation_report.md ו-model_card.md
"""
import os
import sys
import io

# תיקון encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# הוספת נתיב הפרויקט
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crews.data_scientist_crew.tools import ModelEvaluationTool, ModelCardGenerator

def main():
    print("="*60)
    print("Creating evaluation reports and documentation")
    print("="*60)
    
    # בדיקה שהמודל קיים
    model_path = "outputs/model.pkl"
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found: {model_path}")
        return
    
    print(f"\nOK: Model file found: {model_path}")
    
    # יצירת כלי הערכה
    eval_tool = ModelEvaluationTool()
    card_tool = ModelCardGenerator()
    
    # יצירת דוח הערכה
    print("\n" + "="*60)
    print("Creating evaluation_report.md...")
    print("="*60)
    eval_result = eval_tool._run(
        model_path=model_path,
        data_path="outputs/features.csv",
        output_dir="outputs"
    )
    print(eval_result)
    
    # יצירת Model Card
    print("\n" + "="*60)
    print("Creating model_card.md...")
    print("="*60)
    card_result = card_tool._run(
        model_path=model_path,
        comparison_path="outputs/all_models_comparison.json",
        output_dir="outputs"
    )
    print(card_result)
    
    # בדיקה שהקבצים נוצרו
    print("\n" + "="*60)
    if os.path.exists("outputs/evaluation_report.md"):
        print("SUCCESS: evaluation_report.md created!")
    else:
        print("ERROR: evaluation_report.md not created!")
    
    if os.path.exists("outputs/model_card.md"):
        print("SUCCESS: model_card.md created!")
    else:
        print("ERROR: model_card.md not created!")
    
    print("="*60)

if __name__ == "__main__":
    main()

