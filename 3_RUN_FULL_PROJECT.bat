@echo off
chcp 65001 >nul
title House Price Prediction - Full Project
echo.
echo ============================================================
echo   🚀  House Price Prediction - Full Project  🚀
echo ============================================================
echo.
echo זה יריץ את כל הפרויקט (CrewAI Flow)
echo זה עלול לקחת זמן ולהיות כרוך בעלויות API
echo.
echo האם אתה בטוח שברצונך להמשיך? (Y/N)
set /p answer=
if /i "%answer%"=="Y" (
    cd /d "%~dp0"
    python run.py
) else (
    echo בוטל.
)
pause

