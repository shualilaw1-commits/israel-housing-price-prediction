# 🎉 ברוכים הבאים לפרויקט חיזוי מחירי דירות!

## 👋 מה יש לך כאן?

פרויקט **CrewAI מלא ומוכן לשימוש** שכולל:
- ✅ 6 סוכנים אוטונומיים (Agents)
- ✅ 2 צוותים (Crews)
- ✅ Flow אוטומטי
- ✅ 3 מודלי Machine Learning
- ✅ Dashboard אינטראקטיבי
- ✅ תיעוד מקצועי מלא

## ⚡ התחלה מהירה - 3 שלבים בלבד!

### 1️⃣ התקן (פעם אחת)

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

⏱️ **זמן**: 2-3 דקות

🔑 **בונוס**: הקובץ `.env` כבר מוכן עם ה-OpenAI API key שלך!
- ה-Agents יהיו חכמים יותר
- התובנות יהיו מעמיקות יותר
- ראה [API_SETUP.md](API_SETUP.md) לפרטים

### 2️⃣ הרץ את הפרויקט

```bash
python run.py
```

⏱️ **זמן**: 2-5 דקות

**מה קורה?**
- 🔍 Agent 1 טוען נתונים
- 🧹 Agent 2 מנקה נתונים
- 📊 Agent 3 יוצר ויזואליזציות
- 🔧 Agent 4 יוצר פיצ'רים חדשים
- 🤖 Agent 5 מאמן 3 מודלים
- ✅ Agent 6 מעריך ומתעד

**תוצאה**: תיקיית `outputs/` מלאה בקבצים!

### 3️⃣ פתח את ה-Dashboard

```bash
streamlit run app/streamlit_app.py
```

⏱️ **נפתח מיד**: http://localhost:8501

**מה יש שם?**
- 🏠 סקירת הפרויקט
- 📊 חקר נתונים אינטראקטיבי
- 🤖 ביצועי מודלים
- 🎯 חיזוי מחירים - **נסה בעצמך!**

## 📚 רוצה לקרוא יותר?

בחר לפי הרמה שלך:

### 🟢 מתחילים - קרא קודם:
1. **[QUICKSTART_HEBREW.md](QUICKSTART_HEBREW.md)** ← **התחל כאן!**
   - מדריך התחלה מהיר (5 דקות)
   - הכל בעברית, פשוט וברור

### 🟡 ביניים - עיין בהם:
2. **[README_HEBREW.md](README_HEBREW.md)**
   - תיעוד מלא בעברית
   - הסברים מפורטים

3. **[SETUP.md](SETUP.md)**
   - מדריך התקנה מפורט
   - פתרון בעיות נפוצות

### 🔴 מתקדמים - חקור לעומק:
4. **[README.md](README.md)**
   - תיעוד מקצועי באנגלית
   - פרטים טכניים

5. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
   - סיכום טכני של הפרויקט
   - ארכיטקטורה מפורטת

## 🎯 מה הפרויקט עושה?

```
Input: נתוני דירות בקליפורניה
  ↓
6 Agents עובדים ביחד
  ↓
Output: מודל חיזוי + דוחות + Dashboard
```

### הצוותים והסוכנים:

**צוות 1: מנתחי נתונים** 📊
- Agent 1: טוען את הנתונים
- Agent 2: מנקה ומעבד
- Agent 3: יוצר ויזואליזציות ותובנות

**צוות 2: מדעני נתונים** 🤖
- Agent 4: יוצר פיצ'רים חדשים
- Agent 5: מאמן 3 מודלים (Linear, RF, GB)
- Agent 6: מעריך ומתעד את המודל

## 📁 מה יש בתיקיות?

```
house-price-crewai/
├── 📂 crews/          → הצוותים וה-Agents
├── 📂 flow/           → ה-Flow שמחבר ביניהם
├── 📂 app/            → ה-Dashboard
├── 📂 outputs/        → כל התוצרים (נוצר אחרי run.py)
├── 📄 run.py          → הרץ את זה!
└── 📚 מסמכים רבים    → קרא אותם
```

## 🎨 מה תראה ב-Dashboard?

### עמוד 1: 🏠 בית
- סקירה כללית
- מטריקות מרכזיות
- גרפים מהירים

### עמוד 2: 📊 חקר נתונים
- מפה של קליפורניה עם מחירי דירות
- גרפי קורלציות
- התפלגויות
- ועוד...

### עמוד 3: 🤖 ביצועי מודל
- השוואה בין 3 מודלים
- גרפי ביצועים
- דוחות מפורטים

### עמוד 4: 🎯 חיזוי מחיר
- הזן מאפייני דירה
- קבל חיזוי מחיר
- ראה על מפה

**זה החלק הכי מגניב - נסה!** 🚀

## 🆘 נתקעת? תפתור מהר!

### בעיה: "pip install נכשל"
```bash
pip install --no-cache-dir -r requirements.txt
```

### בעיה: "cannot import crewai"
```bash
# ודא שהסביבה הוירטואלית פעילה
# אמור לראות (venv) בתחילת השורה
```

### בעיה: "outputs ריקה"
```bash
# פשוט הרץ שוב
python run.py
```

### בעיה: "Streamlit לא נפתח"
```bash
# נסה פורט אחר
streamlit run app/streamlit_app.py --server.port 8502
```

**עוד בעיות?** קרא [SETUP.md](SETUP.md)

## ✅ Checklist - וודא שעשית הכל

- [ ] התקנת Python 3.8+
- [ ] יצרת סביבה וירטואלית
- [ ] הפעלת את הסביבה (רואה `(venv)`)
- [ ] התקנת חבילות (`pip install -r requirements.txt`)
- [ ] הרצת `python run.py`
- [ ] ראית תיקייה `outputs/` מלאה בקבצים
- [ ] הרצת `streamlit run app/streamlit_app.py`
- [ ] פתחת דפדפן ב-http://localhost:8501
- [ ] חקרת את ה-Dashboard
- [ ] ניסית לעשות חיזוי מחיר בעמוד 4

## 🎓 למה זה טוב לפרויקט גמר?

✅ **CrewAI Flow** - טכנולוגיה מתקדמת
✅ **6 Agents** - מערכת multi-agent מורכבת
✅ **תיעוד מקצועי** - Model Card, Dataset Contract
✅ **Dashboard** - ממשק משתמש מרשים
✅ **ניתן לשחזור** - הכל אוטומטי
✅ **איכות קוד** - מסודר, מתועד, מודולרי

## 💡 טיפים

1. **הרץ `run.py` לפני ה-Dashboard** - צריך את התוצרים קודם
2. **בדוק `outputs/`** - שם כל התוצאות
3. **קרא את ה-markdown files** - בתיקיית outputs יש דוחות מעניינים
4. **שחק עם ה-Dashboard** - עמוד 4 הכי כיפי!
5. **תעד צילומי מסך** - לפרזנטציה

## 🚀 הצעד הבא שלך

### עכשיו מיד:
```bash
python run.py
```

### אחרי שזה מסתיים:
```bash
streamlit run app/streamlit_app.py
```

### אחר כך:
- חקור את התוצרים ב-`outputs/`
- קרא את הדוחות (insights.md, model_card.md)
- שחק עם ה-Dashboard
- הכן פרזנטציה

## 📞 עוד שאלות?

1. קרא [QUICKSTART_HEBREW.md](QUICKSTART_HEBREW.md) - מדריך מפורט
2. עיין ב-[README_HEBREW.md](README_HEBREW.md) - תיעוד מלא
3. בדוק [SETUP.md](SETUP.md) - פתרון בעיות
4. ראה דוגמאות בקוד - הכל מתועד

---

# 🎉 זהו! אתה מוכן!

## הפקודות היחידות שאתה צריך:

```bash
# 1. התקן (פעם אחת)
pip install -r requirements.txt

# 2. הרץ (כל פעם מחדש)
python run.py

# 3. ראה תוצאות (Dashboard)
streamlit run app/streamlit_app.py
```

---

**בהצלחה בפרויקט! 🚀🏠🤖**

*נוצר עם ❤️ באמצעות CrewAI*
