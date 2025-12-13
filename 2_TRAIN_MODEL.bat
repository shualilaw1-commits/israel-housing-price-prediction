@echo off
chcp 65001 >nul
title House Price Prediction - Train Model
echo.
echo ============================================================
echo   🤖  Training Machine Learning Models - Israel  🤖
echo ============================================================
echo.
echo מאמן את המודלים... זה יקח כ-6-7 דקות
echo.
cd /d "%~dp0"
python train_model_manually.py
echo.
echo ============================================================
echo   ✅  האימון הושלם!
echo ============================================================
pause

