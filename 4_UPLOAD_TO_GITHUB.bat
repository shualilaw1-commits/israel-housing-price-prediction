@echo off
chcp 65001 >nul
title Upload to GitHub - Israel Housing Price Prediction
echo.
echo ============================================================
echo   📤  Upload to GitHub - Israel Housing Price  📤
echo ============================================================
echo.
cd /d "%~dp0"

echo [שלב 1/4] בדיקת התחברות ל-GitHub...
gh auth status >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ לא מחובר ל-GitHub!
    echo.
    echo 📝 הוראות:
    echo    1. פתח חלון cmd/PowerShell חדש
    echo    2. הרץ: gh auth login
    echo    3. עקוב אחרי ההוראות על המסך
    echo    4. חזור והרץ קובץ זה שוב
    echo.
    pause
    exit /b 1
)
echo ✅ מחובר ל-GitHub
echo.

echo [שלב 2/4] בדיקת git repository...
git status >nul 2>&1
if errorlevel 1 (
    echo ❌ אין git repository!
    echo מריץ git init...
    git init
    git config user.name "Shuki Shoali"
    git config user.email "shuali.law1@gmail.com"
    git add .
    git commit -m "Initial commit"
)
echo ✅ Git repository קיים
echo.

echo [שלב 3/4] יצירת GitHub repository...
echo.
echo שם הפרויקט: israel-housing-price-prediction
echo תיאור: 🏠 Israel Housing Price Prediction using CrewAI - ML project with 6 autonomous agents
echo.
set /p confirm="האם ליצור repository חדש? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo בוטל.
    pause
    exit /b 0
)

gh repo create israel-housing-price-prediction --public --source=. --remote=origin --description="🏠 Israel Housing Price Prediction using CrewAI - ML project with 6 autonomous agents"
if errorlevel 1 (
    echo.
    echo ⚠️  ייתכן שה-repository כבר קיים או שיש בעיה אחרת.
    echo נסה להריץ ידנית:
    echo    gh repo create israel-housing-price-prediction --public --source=. --remote=origin
    echo.
    echo או צור את ה-repository דרך האתר:
    echo    https://github.com/new
    echo.
    echo ואז הרץ:
    echo    git remote add origin https://github.com/[YOUR-USERNAME]/israel-housing-price-prediction.git
    echo    git push -u origin master
    echo.
    pause
    exit /b 1
)
echo ✅ Repository נוצר ב-GitHub
echo.

echo [שלב 4/4] העלאת קוד ל-GitHub...
git push -u origin master
if errorlevel 1 (
    echo.
    echo ❌ העלאה נכשלה!
    echo נסה להריץ ידנית:
    echo    git push -u origin master
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   ✅  הצלחה! הפרויקט הועלה ל-GitHub!  ✅
echo ============================================================
echo.
echo 🔗 הפרויקט שלך זמין ב:
echo    https://github.com/[YOUR-USERNAME]/israel-housing-price-prediction
echo.
echo 💡 דברים נוספים שכדאי לעשות:
echo    1. הוסף Topics ב-GitHub (settings):
echo       machine-learning, crewai, streamlit, israel, python
echo.
echo    2. הוסף screenshots של ה-Dashboard
echo.
echo    3. שתף את הקישור!
echo.
pause
