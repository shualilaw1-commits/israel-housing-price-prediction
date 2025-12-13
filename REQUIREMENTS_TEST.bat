@echo off
chcp 65001 >nul
title Requirements Test - Project Validation
echo.
echo ============================================================
echo   🧪  Testing Project Requirements  🧪
echo ============================================================
echo.
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 1: Python Environment                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python --version
if errorlevel 1 (
    echo ❌ FAIL: Python not found
    set /a failures+=1
) else (
    echo ✅ PASS: Python installed
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 2: Required Packages                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set packages=crewai pandas numpy scikit-learn streamlit plotly joblib

for %%p in (%packages%) do (
    python -c "import %%p; print('✅ PASS: %%p installed')" 2>nul || (
        echo ❌ FAIL: %%p not installed
        set /a failures+=1
    )
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 3: Project Structure                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set required_dirs=crews flow app outputs

for %%d in (%required_dirs%) do (
    if exist "%%d\" (
        echo ✅ PASS: %%d/ directory exists
    ) else (
        echo ❌ FAIL: %%d/ directory missing
        set /a failures+=1
    )
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 4: Essential Files                                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set required_files=run.py requirements.txt README.md README_HEBREW.md app\streamlit_app.py

for %%f in (%required_files%) do (
    if exist "%%f" (
        echo ✅ PASS: %%f exists
    ) else (
        echo ❌ FAIL: %%f missing
        set /a failures+=1
    )
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 5: CrewAI Components                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

if exist "crews\data_analyst_crew\agents.py" (
    echo ✅ PASS: Data Analyst Crew agents found
) else (
    echo ❌ FAIL: Data Analyst Crew agents missing
    set /a failures+=1
)

if exist "crews\data_scientist_crew\agents.py" (
    echo ✅ PASS: Data Scientist Crew agents found
) else (
    echo ❌ FAIL: Data Scientist Crew agents missing
    set /a failures+=1
)

if exist "flow\housing_flow.py" (
    echo ✅ PASS: CrewAI Flow found
) else (
    echo ❌ FAIL: CrewAI Flow missing
    set /a failures+=1
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 6: Generated Outputs                                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

if exist "outputs\model.pkl" (
    echo ✅ PASS: Trained model found
) else (
    echo ⚠️  WARNING: No trained model (run 2_TRAIN_MODEL.bat)
)

if exist "outputs\dataset_contract.json" (
    echo ✅ PASS: Dataset contract found
) else (
    echo ⚠️  WARNING: No dataset contract (run python run.py)
)

if exist "outputs\model_card.md" (
    echo ✅ PASS: Model card found
) else (
    echo ⚠️  WARNING: No model card (run python run.py)
)

if exist "outputs\evaluation_report.md" (
    echo ✅ PASS: Evaluation report found
) else (
    echo ⚠️  WARNING: No evaluation report (run python run.py)
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 7: Dashboard Components                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python -c "import app.streamlit_app; print('✅ PASS: Dashboard imports successfully')" 2>nul || (
    echo ❌ FAIL: Dashboard has import errors
    set /a failures+=1
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 8: Code Validation                                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python -m py_compile run.py 2>nul
if errorlevel 1 (
    echo ❌ FAIL: run.py has syntax errors
    set /a failures+=1
) else (
    echo ✅ PASS: run.py syntax valid
)

python -m py_compile app\streamlit_app.py 2>nul
if errorlevel 1 (
    echo ❌ FAIL: streamlit_app.py has syntax errors
    set /a failures+=1
) else (
    echo ✅ PASS: streamlit_app.py syntax valid
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 9: Documentation Quality                             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

for %%f in (README.md README_HEBREW.md START_GUIDE.md) do (
    if exist "%%f" (
        for %%A in ("%%f") do (
            if %%~zA GTR 1000 (
                echo ✅ PASS: %%f has substantial content
            ) else (
                echo ⚠️  WARNING: %%f seems short
            )
        )
    ) else (
        echo ❌ FAIL: %%f missing
        set /a failures+=1
    )
)
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  TEST 10: Git Repository                                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

if exist ".git\" (
    echo ✅ PASS: Git repository initialized
    git log --oneline -n 1 2>nul
    if errorlevel 1 (
        echo ⚠️  WARNING: No commits yet
    ) else (
        echo ✅ PASS: Commits found
    )
) else (
    echo ⚠️  WARNING: Not a git repository
)

if exist ".gitignore" (
    echo ✅ PASS: .gitignore exists
) else (
    echo ⚠️  WARNING: No .gitignore file
)
echo.

echo.
echo ============================================================
echo   📊  TEST SUMMARY
echo ============================================================
echo.

if defined failures (
    if %failures% EQU 0 (
        echo ✅ ALL CRITICAL TESTS PASSED!
        echo.
        echo 🎉 Project is ready for submission!
        echo.
        echo Next steps:
        echo   1. Run 1_RUN_DASHBOARD.bat to test dashboard
        echo   2. Run 4_UPLOAD_TO_GITHUB.bat to upload
        echo   3. Submit repository URL
    ) else (
        echo ❌ FOUND %failures% CRITICAL FAILURES
        echo.
        echo ⚠️  Please fix the failures above before submitting
        echo.
        echo Common fixes:
        echo   - Install missing packages: pip install -r requirements.txt
        echo   - Run: python run.py (to generate outputs)
        echo   - Run: python train_model_manually.py (to train model)
    )
) else (
    echo ✅ ALL CRITICAL TESTS PASSED!
    echo.
    echo 🎉 Project is ready for submission!
)

echo.
echo ============================================================
pause
