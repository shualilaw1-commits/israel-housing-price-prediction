# 🔑 הגדרת API Key

## ✅ הקובץ .env כבר נוצר!

הקובץ `.env` כבר מוכן עם ה-OpenAI API key שלך.

## 📋 מה יש בקובץ .env?

```env
OPENAI_API_KEY=sk-proj-...
CREWAI_TELEMETRY_OPT_OUT=true
PROJECT_NAME=house-price-prediction
DEBUG=false
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
```

## 🔒 אבטחה - חשוב!

⚠️ **הקובץ .env כבר ב-.gitignore** - לא יעלה ל-Git

✅ ה-API key שלך מוגן ולא ישותף בטעות

## 🎯 איך זה עובד?

1. **הפרויקט טוען את .env אוטומטית**
   - `run.py` טוען את המשתנים
   - `flow/housing_flow.py` טוען את המשתנים
   - כל ה-agents מקבלים גישה ל-API

2. **ה-Agents ישתמשו ב-GPT**
   - במקום agents "דמה", יהיה לך AI אמיתי
   - התשובות יהיו חכמות יותר
   - הניתוחים יהיו מעמיקים יותר

## 🚀 איך להריץ עם API?

פשוט תריץ כרגיל:

```bash
# הכל אוטומטי!
python run.py
```

הפרויקט ישתמש ב-API key שלך אוטומטית.

## 💰 שימוש ב-API

### מודל המוגדר
- **GPT-4 Turbo Preview** - מודל חכם ומהיר
- **Temperature: 0.7** - איזון בין יצירתיות ודיוק

### עלויות צפויות
עבור הרצה אחת של הפרויקט:
- ~0.01-0.05$ (1-5 סנט)
- תלוי באורך הניתוחים

### מעקב אחר שימוש
בדוק ב-[OpenAI Dashboard](https://platform.openai.com/usage)

## 🔧 התאמה אישית

### שנה מודל

ערוך `.env`:
```env
MODEL_NAME=gpt-3.5-turbo  # זול יותר
# או
MODEL_NAME=gpt-4          # חכם יותר
```

### שנה Temperature

```env
TEMPERATURE=0.3  # יותר דטרמיניסטי
# או
TEMPERATURE=0.9  # יותר יצירתי
```

## 🔄 שימוש עם ספקים אחרים

### Anthropic (Claude)

הוסף ל-`.env`:
```env
ANTHROPIC_API_KEY=your_key_here
```

### Groq (מהיר וחינמי)

הוסף ל-`.env`:
```env
GROQ_API_KEY=your_key_here
```

## ❌ בעיות נפוצות

### "OpenAI API key not found"

**פתרון**:
```bash
# ודא שהקובץ .env קיים
ls -la .env

# בדוק שיש תוכן
cat .env
```

### "Rate limit exceeded"

**פתרון**:
- המתן דקה
- או שנה ל-gpt-3.5-turbo (יותר quota)

### "Invalid API key"

**פתרון**:
1. בדוק ב-[OpenAI Platform](https://platform.openai.com/api-keys)
2. צור key חדש אם צריך
3. עדכן ב-`.env`

## 🎨 הבדלים עם/בלי API

### בלי API (ברירת מחדל)
- ✓ עובד מקומית
- ✓ חינם לגמרי
- ✗ Agents פחות "חכמים"
- ✗ ניתוחים בסיסיים יותר

### עם API (מומלץ)
- ✓ Agents חכמים מאוד
- ✓ ניתוחים מעמיקים
- ✓ תובנות איכוותיות
- ✗ עולה כסף (מעט)

## 📊 מה ישתפר עם API?

1. **EDA Agent**
   - תובנות עמוקות יותר
   - המלצות מדויקות יותר

2. **Feature Engineer**
   - פיצ'רים יצירתיים יותר
   - הסברים טובים יותר

3. **Model Evaluator**
   - ניתוח מפורט יותר
   - Model Card עשיר יותר

## ✅ אימות שה-API עובד

הרץ:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

אמור לראות:
```
API Key: sk-proj-6v...
```

## 🎯 סיכום

✅ הקובץ `.env` מוכן
✅ ה-API key נטען אוטומטית
✅ הפרויקט ישתמש ב-GPT
✅ הכל מאובטח (לא יעלה ל-Git)

**פשוט תריץ `python run.py` ותיהנה מ-AI חכם! 🚀**

---

**צריך עזרה?** קרא את [START_HERE.md](START_HERE.md)
