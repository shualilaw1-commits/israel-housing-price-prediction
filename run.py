"""
Run Script - הרצת הפרויקט המלא
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Fix encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# הוספת נתיב הפרויקט
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from flow.housing_flow import HousePricePredictionFlow


def print_banner():
    """מדפיס כותרת פתיחה"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║      🏠  California Housing Price Prediction Project  🏠      ║
    ║                                                              ║
    ║                  CrewAI Flow with 6 Agents                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

    תאריך הרצה: {date}

    הפרויקט כולל:
    ✓ 2 Crews (צוותים)
    ✓ 6 Agents (סוכנים אוטונומיים)
    ✓ Dataset Contract
    ✓ Feature Engineering
    ✓ 3 מודלי ML שונים
    ✓ Model Card מקצועי
    ✓ ממשק Streamlit

    """.format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print(banner)


def check_environment():
    """בודק שהסביבה מוכנה"""
    print("🔍 בודק סביבת הפעלה...\n")

    checks = []

    # בדיקת Python version
    import sys
    py_version = sys.version_info
    if py_version.major == 3 and py_version.minor >= 8:
        checks.append(("✓", f"Python {py_version.major}.{py_version.minor}.{py_version.micro}"))
    else:
        checks.append(("✗", f"Python {py_version.major}.{py_version.minor} - נדרש 3.8+"))

    # בדיקת packages חשובים
    packages_to_check = [
        'crewai',
        'pandas',
        'sklearn',
        'streamlit',
        'plotly'
    ]

    for package in packages_to_check:
        try:
            __import__(package)
            checks.append(("✓", f"{package} מותקן"))
        except ImportError:
            checks.append(("✗", f"{package} חסר - הרץ: pip install -r requirements.txt"))

    # בדיקת תיקיית outputs
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        checks.append(("✓", "תיקיית outputs נוצרה"))
    else:
        checks.append(("✓", "תיקיית outputs קיימת"))

    # הצגת תוצאות
    for symbol, message in checks:
        print(f"  {symbol} {message}")

    print()

    # בדיקה אם יש בעיות
    if any(check[0] == "✗" for check in checks):
        print("❌ יש בעיות בסביבת ההפעלה. אנא תקן אותן לפני ההמשך.\n")
        return False

    print("✓ הסביבה מוכנה!\n")
    return True


def run_pipeline():
    """מריץ את כל ה-Pipeline"""
    try:
        # הדפסת כותרת
        print_banner()

        # בדיקת סביבה
        if not check_environment():
            return False

        # הרצת ה-Flow
        print("="*60)
        print("🚀 מתחיל הרצת Flow...")
        print("="*60)
        print()

        flow = HousePricePredictionFlow()
        result = flow.kickoff()

        print()
        print("="*60)
        print("✅ ה-Pipeline הושלם בהצלחה!")
        print("="*60)
        print()

        # סיכום
        print_summary()

        return True

    except KeyboardInterrupt:
        print("\n\n⚠️  הפעלה בוטלה על ידי המשתמש\n")
        return False

    except Exception as e:
        print(f"\n\n❌ שגיאה בהרצת ה-Pipeline: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def print_summary():
    """מדפיס סיכום התוצרים"""
    summary = """
    📁 כל התוצרים נמצאים בתיקייה: outputs/

    📊 נתונים:
       - raw_data.csv         (נתונים גולמיים)
       - clean_data.csv       (נתונים מנוקים)
       - features.csv         (עם פיצ'רים מהונדסים)

    📋 תיעוד:
       - dataset_contract.json           (חוזה נתונים)
       - insights.md                     (תובנות EDA)
       - feature_engineering_report.md   (דוח הנדסת פיצ'רים)
       - evaluation_report.md            (דוח הערכת מודל)
       - model_card.md                   (Model Card מקצועי)

    🤖 מודלים:
       - model.pkl                       (המודל הטוב ביותר)
       - all_models_comparison.json      (השוואת כל המודלים)

    📈 ויזואליזציות:
       - figures/                        (גרפי EDA)
       - evaluation_figures/             (גרפי הערכת מודל)

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    🎯 מה הלאה?

    1️⃣  הרץ את ה-Dashboard:
        streamlit run app/streamlit_app.py

    2️⃣  צפה בתוצאות:
        - עיין בקבצי ה-Markdown (insights.md, model_card.md וכו')
        - פתח את הגרפים בתיקיות figures

    3️⃣  התאם אישית:
        - ערוך את ה-agents בתיקיות crews/
        - שנה פרמטרים ב-tasks.py
        - הוסף פיצ'רים חדשים ב-tools.py

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(summary)


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
