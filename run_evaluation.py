# -*- coding: utf-8 -*-
import os
import sys
import io

# Fix encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crews.data_scientist_crew.tools import ModelEvaluationTool, ModelCardGenerator

def main():
    print("="*60)
    print("Creating evaluation reports")
    print("="*60)
    
    model_path = "outputs/model.pkl"
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found: {model_path}")
        return
    
    print(f"OK: Model found")
    
    # Create evaluation report
    print("\nCreating evaluation_report.md...")
    eval_tool = ModelEvaluationTool()
    result1 = eval_tool._run(
        model_path=model_path,
        data_path="outputs/features.csv",
        output_dir="outputs"
    )
    print(result1)
    
    # Create model card
    print("\nCreating model_card.md...")
    card_tool = ModelCardGenerator()
    result2 = card_tool._run(
        model_path=model_path,
        comparison_path="outputs/all_models_comparison.json",
        output_dir="outputs"
    )
    print(result2)
    
    # Check results
    print("\n" + "="*60)
    if os.path.exists("outputs/evaluation_report.md"):
        print("SUCCESS: evaluation_report.md created")
    else:
        print("ERROR: evaluation_report.md NOT created")
    
    if os.path.exists("outputs/model_card.md"):
        print("SUCCESS: model_card.md created")
    else:
        print("ERROR: model_card.md NOT created")
    print("="*60)

if __name__ == "__main__":
    main()

