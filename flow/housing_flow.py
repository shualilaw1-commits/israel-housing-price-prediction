"""
House Price Prediction Flow - מחבר בין צוות מנתחי הנתונים לצוות מדעני הנתונים
"""
import os
import json
from dotenv import load_dotenv
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from typing import Dict, Any

# טעינת משתני סביבה
load_dotenv()

# ייבוא הצוותים
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crews.data_analyst_crew import DataAnalystCrew
from crews.data_scientist_crew import DataScientistCrew


class FlowState(BaseModel):
    """מצב ה-Flow - שומר מידע בין שלבים"""
    dataset_loaded: bool = False
    data_cleaned: bool = False
    eda_completed: bool = False
    features_created: bool = False
    model_trained: bool = False
    evaluation_completed: bool = False

    # נתיבים לקבצים
    clean_data_path: str = ""
    features_path: str = ""
    model_path: str = ""

    # תוצאות
    data_analysis_result: Dict[str, Any] = {}
    modeling_result: Dict[str, Any] = {}


class HousePricePredictionFlow(Flow[FlowState]):
    """
    Flow מלא לחיזוי מחירי דירות

    שלבים:
    1. Data Analyst Crew - ניתוח וחקר הנתונים
    2. Validation - וולידציה של הנתונים
    3. Data Scientist Crew - בניית והערכת מודלים
    """

    @start()
    def start_flow(self):
        """נקודת התחלה של ה-Flow"""
        print("\n" + "="*60)
        print("🚀 מתחיל Flow לחיזוי מחירי דירות")
        print("="*60 + "\n")

        # אתחול מצב
        self.state.dataset_loaded = False
        self.state.data_cleaned = False
        self.state.eda_completed = False

        # יצירת תיקיית outputs
        os.makedirs("outputs", exist_ok=True)

        return "Data analysis ready to start"

    @listen(start_flow)
    def run_data_analyst_crew(self, message: str):
        """שלב 1: הרצת צוות מנתחי הנתונים"""
        print("\n" + "="*60)
        print("📊 שלב 1: צוות מנתחי הנתונים")
        print("="*60 + "\n")

        try:
            # הרצת הצוות
            analyst_crew = DataAnalystCrew()
            result = analyst_crew.run()

            # עדכון מצב
            self.state.data_cleaned = True
            self.state.eda_completed = True
            self.state.clean_data_path = "outputs/clean_data.csv"
            self.state.data_analysis_result = result

            print("\n✓ צוות מנתחי הנתונים סיים בהצלחה!")
            print(f"  - נתונים מנוקים: {self.state.clean_data_path}")
            print(f"  - תובנות: outputs/insights.md")
            print(f"  - גרפים: outputs/figures/")

            return "Data analysis completed successfully"

        except Exception as e:
            print(f"\n❌ שגיאה בצוות מנתחי הנתונים: {str(e)}")
            raise

    @listen(run_data_analyst_crew)
    def validate_data(self, message: str):
        """שלב 2: וולידציה של הנתונים לפני מעבר לשלב הבא"""
        print("\n" + "="*60)
        print("✅ שלב 2: וולידציה של הנתונים")
        print("="*60 + "\n")

        # בדיקה שקובץ הנתונים המנוקים קיים
        if not os.path.exists(self.state.clean_data_path):
            raise FileNotFoundError(f"קובץ נתונים מנוקים לא נמצא: {self.state.clean_data_path}")

        # בדיקה שקובץ החוזה קיים
        contract_path = "outputs/dataset_contract.json"
        if not os.path.exists(contract_path):
            raise FileNotFoundError(f"Dataset contract לא נמצא: {contract_path}")

        # קריאת החוזה
        with open(contract_path, 'r', encoding='utf-8') as f:
            contract = json.load(f)

        # בדיקות וולידציה
        validations = []

        # בדיקה 1: יש מספיק שורות?
        num_rows = contract.get('cleaning', {}).get('cleaned_rows', 0)
        if num_rows < 1000:
            validations.append(f"⚠️  אזהרה: רק {num_rows} שורות - פחות מהמינימום המומלץ (1000)")
        else:
            validations.append(f"✓ מספר שורות תקין: {num_rows:,}")

        # בדיקה 2: יש עמודת target?
        columns = contract.get('columns', {})
        if 'Price_Millions' not in columns:
            raise ValueError("עמודת Target (Price_Millions) חסרה!")
        validations.append("✓ עמודת Target קיימת")

        # בדיקה 3: אין יותר מדי ערכים חסרים?
        missing = contract.get('cleaning', {}).get('missing_values_found', {})
        if missing:
            validations.append(f"⚠️  זוהו {len(missing)} עמודות עם ערכים חסרים (טופלו)")
        else:
            validations.append("✓ אין ערכים חסרים")

        print("תוצאות וולידציה:")
        for v in validations:
            print(f"  {v}")

        print("\n✓ וולידציה עברה בהצלחה - ממשיכים לשלב הבא\n")

        return "Data validation passed"

    @listen(validate_data)
    def run_data_scientist_crew(self, message: str):
        """שלב 3: הרצת צוות מדעני הנתונים"""
        print("\n" + "="*60)
        print("🤖 שלב 3: צוות מדעני הנתונים")
        print("="*60 + "\n")

        try:
            # הרצת הצוות
            scientist_crew = DataScientistCrew()
            result = scientist_crew.run()

            # עדכון מצב
            self.state.features_created = True
            self.state.model_trained = True
            self.state.evaluation_completed = True
            self.state.features_path = "outputs/features.csv"
            self.state.model_path = "outputs/model.pkl"
            self.state.modeling_result = result

            print("\n✓ צוות מדעני הנתונים סיים בהצלחה!")
            print(f"  - פיצ'רים: {self.state.features_path}")
            print(f"  - מודל: {self.state.model_path}")
            print(f"  - דוח הערכה: outputs/evaluation_report.md")
            print(f"  - Model Card: outputs/model_card.md")

            return "Model training and evaluation completed"

        except Exception as e:
            print(f"\n❌ שגיאה בצוות מדעני הנתונים: {str(e)}")
            raise

    @listen(run_data_scientist_crew)
    def finalize_flow(self, message: str):
        """שלב 4: סיום ה-Flow"""
        print("\n" + "="*60)
        print("🎉 ה-Flow הושלם בהצלחה!")
        print("="*60 + "\n")

        # סיכום כל התוצרים
        outputs = {
            "נתונים": [
                "outputs/raw_data.csv",
                "outputs/clean_data.csv",
                "outputs/features.csv"
            ],
            "תיעוד": [
                "outputs/dataset_contract.json",
                "outputs/insights.md",
                "outputs/feature_engineering_report.md",
                "outputs/evaluation_report.md",
                "outputs/model_card.md"
            ],
            "מודלים": [
                "outputs/model.pkl",
                "outputs/all_models_comparison.json"
            ],
            "ויזואליזציות": [
                "outputs/figures/",
                "outputs/evaluation_figures/"
            ]
        }

        print("📁 כל התוצרים שנוצרו:\n")
        for category, files in outputs.items():
            print(f"{category}:")
            for file in files:
                exists = "✓" if os.path.exists(file) else "✗"
                print(f"  {exists} {file}")

        # שמירת סיכום ה-Flow
        flow_summary = {
            "flow_completed": True,
            "timestamp": str(os.path.getctime("outputs")),
            "state": {
                "dataset_loaded": self.state.dataset_loaded,
                "data_cleaned": self.state.data_cleaned,
                "eda_completed": self.state.eda_completed,
                "features_created": self.state.features_created,
                "model_trained": self.state.model_trained,
                "evaluation_completed": self.state.evaluation_completed
            },
            "outputs": outputs
        }

        with open("outputs/flow_summary.json", 'w', encoding='utf-8') as f:
            json.dump(flow_summary, f, ensure_ascii=False, indent=2)

        print("\n✓ סיכום Flow נשמר ב: outputs/flow_summary.json")
        print("\n🎯 הפרויקט מוכן! אפשר להריץ את ה-Streamlit dashboard:\n")
        print("   streamlit run app/streamlit_app.py\n")

        return "Flow completed successfully"


def run_flow():
    """פונקציה עזר להרצת ה-Flow"""
    flow = HousePricePredictionFlow()
    result = flow.kickoff()
    return result


if __name__ == "__main__":
    run_flow()
