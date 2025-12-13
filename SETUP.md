# 🔧 Setup Guide - מדריך התקנה מפורט

## דרישות מקדימות

### 1. Python
- **גרסה נדרשת**: Python 3.8 ומעלה
- **בדיקה**:
  ```bash
  python --version
  ```

### 2. Git (אופציונלי)
- לניהול גרסאות
- [הורדה](https://git-scm.com/)

## שלבי ההתקנה

### שלב 1: הורדת הפרויקט

אם קיבלת קובץ tar.gz:
```bash
tar -xzf house-price-crewai.tar.gz
cd house-price-crewai
```

אם קלונת מ-Git:
```bash
git clone <repository-url>
cd house-price-crewai
```

### שלב 2: סביבה וירטואלית

#### Windows:
```bash
# יצירת סביבה
python -m venv venv

# הפעלה
venv\Scripts\activate

# אמת שהסביבה פעילה (תראה (venv) בתחילת השורה)
```

#### Mac/Linux:
```bash
# יצירת סביבה
python3 -m venv venv

# הפעלה
source venv/bin/activate

# אמת שהסביבה פעילה
```

### שלב 3: התקנת חבילות

```bash
# שדרג pip
pip install --upgrade pip

# התקן את כל התלויות
pip install -r requirements.txt
```

**זמן משוער**: 2-5 דקות

### שלב 4: אימות ההתקנה

```bash
python -c "import crewai; import pandas; import sklearn; print('✓ All packages installed successfully!')"
```

אם אין שגיאות - הכל מוכן! ✅

## הרצה ראשונה

### 1. הרץ את ה-Pipeline

```bash
python run.py
```

**תוצאה צפויה**:
- הדפסת banner
- בדיקת סביבה
- הרצת 6 agents
- יצירת כל התוצרים ב-`outputs/`

**זמן ריצה**: 2-5 דקות

### 2. בדוק את התוצאות

```bash
# Windows
dir outputs

# Mac/Linux
ls -la outputs
```

אמור לראות:
- clean_data.csv
- model.pkl
- insights.md
- ועוד...

### 3. הרץ את ה-Dashboard

```bash
streamlit run app/streamlit_app.py
```

**יפתח בדפדפן**: http://localhost:8501

## פתרון בעיות נפוצות

### בעיה 1: pip install נכשל

**פתרון**:
```bash
pip install --no-cache-dir -r requirements.txt
```

### בעיה 2: ModuleNotFoundError

**פתרון**:
```bash
# ודא שהסביבה הוירטואלית פעילה
# אמור לראות (venv) בתחילת השורה

# התקן שוב את החבילה החסרה
pip install <package-name>
```

### בעיה 3: CrewAI import error

**פתרון**:
```bash
pip install crewai==0.86.0 --force-reinstall
```

### בעיה 4: Streamlit לא נפתח

**פתרון**:
```bash
# בדוק שהפורט לא תפוס
streamlit run app/streamlit_app.py --server.port 8502
```

### בעיה 5: התיקייה outputs ריקה

**פתרון**:
הרץ שוב:
```bash
python run.py
```

## הגדרות מתקדמות

### שימוש ב-API Keys (אופציונלי)

אם תרצה להשתמש ב-LLM אמיתי (GPT, Claude וכו'):

1. העתק את `.env.example`:
```bash
cp .env.example .env
```

2. ערוך את `.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**הערה**: הפרויקט פועל גם בלי API keys, אבל ה-agents יהיו פחות "חכמים"

### שינוי הגדרות

ערוך את הקבצים:
- `crews/*/agents.py` - שינוי agents
- `crews/*/tasks.py` - שינוי משימות
- `flow/housing_flow.py` - שינוי תהליך העבודה

## בדיקה שהכל עובד

הרץ את הפקודות הבאות:

```bash
# 1. בדוק Python
python --version

# 2. בדוק pip
pip --version

# 3. בדוק חבילות
pip list | grep crewai
pip list | grep pandas
pip list | grep streamlit

# 4. בדוק מבנה הפרויקט
tree -L 2  # Linux/Mac
# או
dir /s /b  # Windows

# 5. הרץ את הפרויקט
python run.py
```

## שאלות נפוצות

**Q: כמה זמן לוקחת ההתקנה?**
A: 5-10 דקות כולל הורדת חבילות

**Q: כמה זמן לוקחת הרצה?**
A: 2-5 דקות להרצה מלאה

**Q: האם צריך אינטרנט?**
A: כן, להתקנת חבילות ולהורדת dataset

**Q: כמה מקום דיסק נדרש?**
A: ~500MB (חבילות + נתונים + תוצרים)

**Q: האם אפשר להריץ על Mac/Linux?**
A: כן! הפרויקט תומך ב-Windows, Mac ו-Linux

## עזרה נוספת

אם נתקעת:

1. **בדוק את הלוגים** - קרא את השגיאות בעיון
2. **חפש בגוגל** - רוב השגיאות מוכרות
3. **בדוק requirements** - אולי חבילה חסרה
4. **התחל מחדש** - לפעמים עוזר למחוק venv ולהתקין מחדש

---

**בהצלחה! 🚀**
