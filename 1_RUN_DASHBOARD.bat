@echo off
chcp 65001 >nul
title House Price Prediction - Dashboard
echo.
echo ============================================================
echo   🏠  House Price Prediction Dashboard - Israel  🏠
echo ============================================================
echo.
echo מפעיל את ה-Dashboard...
echo.
cd /d "%~dp0"
python -m streamlit run app/streamlit_app.py
pause

