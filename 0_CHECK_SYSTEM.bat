@echo off
chcp 65001 >nul
title System Check - House Price Prediction
echo.
echo ============================================================
echo   🔍  בדיקת מערכת - House Price Prediction  🔍
echo ============================================================
echo.
echo מבצע בדיקת מערכת...
echo.
cd /d "%~dp0"

echo [1/5] בדיקת Python...
python --version
if errorlevel 1 (
    echo ❌ Python לא מותקן!
    echo אנא התקן Python 3.11 או חדש יותר
    pause
    exit /b 1
)
echo ✅ Python מותקן
echo.

echo [2/5] בדיקת חבילות חיוניות...
python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)" 2>nul || echo ❌ Streamlit חסר - הרץ: pip install -r requirements.txt
python -c "import pandas; print('✅ Pandas:', pandas.__version__)" 2>nul || echo ❌ Pandas חסר - הרץ: pip install -r requirements.txt
python -c "import sklearn; print('✅ Scikit-learn:', sklearn.__version__)" 2>nul || echo ❌ Scikit-learn חסר - הרץ: pip install -r requirements.txt
python -c "import plotly; print('✅ Plotly:', plotly.__version__)" 2>nul || echo ❌ Plotly חסר - הרץ: pip install -r requirements.txt
echo.

echo [3/5] בדיקת קבצים חיוניים...
if exist "app\streamlit_app.py" (echo ✅ streamlit_app.py קיים) else (echo ❌ streamlit_app.py חסר!)
if exist "train_model_manually.py" (echo ✅ train_model_manually.py קיים) else (echo ❌ train_model_manually.py חסר!)
if exist "run.py" (echo ✅ run.py קיים) else (echo ❌ run.py חסר!)
if exist "requirements.txt" (echo ✅ requirements.txt קיים) else (echo ❌ requirements.txt חסר!)
echo.

echo [4/5] בדיקת תיקיית outputs...
if exist "outputs" (
    echo ✅ תיקיית outputs קיימת
    if exist "outputs\model.pkl" (echo   ✅ model.pkl קיים) else (echo   ⚠️  model.pkl חסר - הרץ: 2_TRAIN_MODEL.bat)
    if exist "outputs\clean_data.csv" (echo   ✅ clean_data.csv קיים) else (echo   ⚠️  clean_data.csv חסר - הרץ: python run.py)
    if exist "outputs\features.csv" (echo   ✅ features.csv קיים) else (echo   ⚠️  features.csv חסר - הרץ: python run.py)
) else (
    echo ⚠️  תיקיית outputs חסרה - הרץ: python run.py
)
echo.

echo [5/5] בדיקת קובץ .env (אופציונלי)...
if exist ".env" (
    echo ✅ קובץ .env קיים
    findstr /C:"OPENAI_API_KEY" .env >nul 2>nul
    if errorlevel 1 (
        echo   ⚠️  OPENAI_API_KEY לא נמצא ב-.env
    ) else (
        echo   ✅ OPENAI_API_KEY מוגדר
    )
) else (
    echo ⚠️  קובץ .env לא קיים - נדרש רק ל-CrewAI (3_RUN_FULL_PROJECT)
)
echo.

echo ============================================================
echo   📊  סיכום בדיקת מערכת
echo ============================================================
echo.
echo אם כל הבדיקות עברו בהצלחה (✅), המערכת מוכנה!
echo.
echo שלבים הבאים:
echo   1. לחץ על 1_RUN_DASHBOARD.bat להפעלת הממשק
echo   2. אם חסרים קבצים, לחץ על 2_TRAIN_MODEL.bat
echo   3. לפרויקט מלא עם CrewAI, לחץ על 3_RUN_FULL_PROJECT.bat
echo.
echo ============================================================
pause
