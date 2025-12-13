# 📚 מפת הפרויקט - לאן ללכת?

## 🎯 אתה חדש? **התחל כאן!**

### ⭐ הקובץ החשוב ביותר:
📄 **[START_HERE.md](START_HERE.md)** ← **קרא את זה ראשון!**

---

## 📖 מדריכים לפי רמה

### 🟢 רמה 1: מתחילים (5-10 דקות)

1. **[START_HERE.md](START_HERE.md)**
   - נקודת התחלה
   - 3 שלבים פשוטים
   - Checklist

2. **[QUICKSTART_HEBREW.md](QUICKSTART_HEBREW.md)**
   - התחלה מהירה בעברית
   - הוראות ברורות
   - פתרון בעיות נפוצות

🔑 **[API_SETUP.md](API_SETUP.md)** - הגדרת API (אופציונלי אבל מומלץ)
   - הקובץ .env כבר מוכן!
   - שימוש ב-OpenAI GPT
   - Agents חכמים יותר

### 🟡 רמה 2: ביניים (20-30 דקות)

3. **[README_HEBREW.md](README_HEBREW.md)**
   - תיעוד מלא בעברית
   - הסברים על הארכיטקטורה
   - דוגמאות קוד

4. **[SETUP.md](SETUP.md)**
   - התקנה מפורטת
   - פתרון בעיות
   - הגדרות מתקדמות

### 🔴 רמה 3: מתקדמים (1-2 שעות)

5. **[README.md](README.md)**
   - תיעוד מקצועי באנגלית
   - פרטים טכניים
   - Best practices

6. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
   - סיכום טכני מקיף
   - ארכיטקטורה מפורטת
   - כל הקבצים והתלויות

---

## 📂 מדריך לקבצי הקוד

### Core Files (חובה להבין)

| קובץ | תיאור | מתי לקרוא |
|------|-------|-----------|
| [run.py](run.py) | הרצה ראשית | כשרוצה להריץ |
| [flow/housing_flow.py](flow/housing_flow.py) | Flow ראשי | להבנת התזרים |

### Data Analyst Crew (צוות 1)

| קובץ | תיאור | מה יש בפנים |
|------|-------|-------------|
| [crews/data_analyst_crew/agents.py](crews/data_analyst_crew/agents.py) | 3 agents | Ingestion, Cleaning, EDA |
| [crews/data_analyst_crew/tasks.py](crews/data_analyst_crew/tasks.py) | 3 tasks | מה כל agent עושה |
| [crews/data_analyst_crew/tools.py](crews/data_analyst_crew/tools.py) | 4 tools | הכלים של ה-agents |
| [crews/data_analyst_crew/crew.py](crews/data_analyst_crew/crew.py) | Crew | ניהול הצוות |

### Data Scientist Crew (צוות 2)

| קובץ | תיאור | מה יש בפנים |
|------|-------|-------------|
| [crews/data_scientist_crew/agents.py](crews/data_scientist_crew/agents.py) | 3 agents | Engineer, Trainer, Evaluator |
| [crews/data_scientist_crew/tasks.py](crews/data_scientist_crew/tasks.py) | 3 tasks | מה כל agent עושה |
| [crews/data_scientist_crew/tools.py](crews/data_scientist_crew/tools.py) | 8 tools | הכלים של ה-agents |
| [crews/data_scientist_crew/crew.py](crews/data_scientist_crew/crew.py) | Crew | ניהול הצוות |

### Dashboard

| קובץ | תיאור | מה יש בפנים |
|------|-------|-------------|
| [app/streamlit_app.py](app/streamlit_app.py) | Streamlit App | 4 עמודים אינטראקטיביים |

---

## 🎓 לפי מטרה

### רוצה **להריץ** את הפרויקט?
1. קרא: [START_HERE.md](START_HERE.md)
2. הרץ: `python run.py`
3. Dashboard: `streamlit run app/streamlit_app.py`

### רוצה **להבין** איך זה עובד?
1. קרא: [README_HEBREW.md](README_HEBREW.md)
2. עיין ב-: [flow/housing_flow.py](flow/housing_flow.py)
3. חקור: [crews/*/agents.py](crews/)

### רוצה **לשנות** משהו?
1. קרא: [README.md](README.md)
2. ערוך: [crews/*/agents.py](crews/) או [crews/*/tools.py](crews/)
3. בדוק: `python run.py`

### רוצה **להרחיב**?
1. קרא: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. הוסף: agent/tool/task חדש
3. עדכן: [flow/housing_flow.py](flow/housing_flow.py)

---

## 🔍 חיפוש מהיר

### "איך מתקינים?"
→ [SETUP.md](SETUP.md) סעיף "שלבי ההתקנה"

### "מה עושה כל agent?"
→ [README_HEBREW.md](README_HEBREW.md) סעיף "הסוכנים (Agents)"

### "איך להוסיף agent חדש?"
→ [README.md](README.md) סעיף "Customization"

### "מה הקבצים בoutputs?"
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) סעיף "מבנה הפרויקט"

### "איך ה-Flow עובד?"
→ [README_HEBREW.md](README_HEBREW.md) סעיף "ארכיטקטורה"

### "יש שגיאה!"
→ [SETUP.md](SETUP.md) סעיף "פתרון בעיות נפוצות"

---

## 📊 מפת תהליך העבודה

```
קרא START_HERE.md
       ↓
התקן חבילות
       ↓
הרץ python run.py
       ↓
   בדוק outputs/
       ↓
הרץ streamlit
       ↓
   שחק עם Dashboard
       ↓
קרא README_HEBREW.md להבנה
       ↓
   הבן את הקוד
       ↓
שנה/הרחב (אופציונלי)
```

---

## 🎯 קבצים לפי שימוש

### להרצה
- `run.py` - הרצה ראשית
- `requirements.txt` - התקנת חבילות
- `app/streamlit_app.py` - Dashboard

### לקריאה
- `START_HERE.md` - התחלה
- `README_HEBREW.md` - תיעוד עברית
- `README.md` - תיעוד אנגלית
- `PROJECT_SUMMARY.md` - סיכום טכני

### למידע
- `QUICKSTART_HEBREW.md` - התחלה מהירה
- `SETUP.md` - מדריך התקנה
- `.env.example` - דוגמת משתני סביבה

### לפיתוח
- כל הקבצים ב-`crews/` - הצוותים
- `flow/housing_flow.py` - ה-Flow
- `app/streamlit_app.py` - ה-Dashboard

---

## ⚡ טיפים מהירים

💡 **חדש לגמרי?** → [START_HERE.md](START_HERE.md)

💡 **רוצה להבין?** → [README_HEBREW.md](README_HEBREW.md)

💡 **יש בעיה?** → [SETUP.md](SETUP.md)

💡 **רוצה לשנות?** → [README.md](README.md)

💡 **רוצה פרטים?** → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 📞 סדר קריאה מומלץ

### מסלול מהיר (30 דקות)
1. START_HERE.md (5 דק')
2. הרץ python run.py (5 דק')
3. הרץ streamlit (2 דק')
4. שחק עם Dashboard (15 דק')
5. קרא insights.md בoutputs (3 דק')

### מסלול מלא (2 שעות)
1. START_HERE.md
2. QUICKSTART_HEBREW.md
3. הרץ את הפרויקט
4. README_HEBREW.md
5. עיון בקוד
6. SETUP.md
7. PROJECT_SUMMARY.md

### מסלול למפתחים (4+ שעות)
1. כל הקבצים לעיל
2. README.md
3. קריאת כל הקוד
4. התנסות בשינויים
5. הרחבות

---

## ✅ Checklist למתחילים

- [ ] קראתי START_HERE.md
- [ ] התקנתי את החבילות
- [ ] הרצתי python run.py
- [ ] ראיתי outputs/ מלאה
- [ ] הרצתי את ה-Dashboard
- [ ] שיחקתי עם עמוד החיזוי
- [ ] קראתי README_HEBREW.md
- [ ] הבנתי את הארכיטקטורה
- [ ] עיינתי בקוד
- [ ] מוכן להציג!

---

**מוכן להתחיל? לך ל-[START_HERE.md](START_HERE.md)! 🚀**
