@echo off
title EvidenceGuard AI – NBA Accreditation Faculty Agent
color 0A

echo.
echo ============================================================
echo   EvidenceGuard AI – NBA Accreditation Faculty Agent
echo   IBM AICTE Agentic AI Project
echo   NBA Knowledge Base: May 2026 Edition / GAPC v4.0
echo ============================================================
echo.

REM ── Step 1: Check Python ─────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please download Python 3.9 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python found.

REM ── Step 2: Install required packages ────────────────────────────────────
echo.
echo [INFO] Installing Python dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] Core dependencies installed (Flask, Flask-CORS).

REM ── Step 3: Optional IBM Granite SDK ─────────────────────────────────────
echo.
echo [INFO] Checking IBM watsonx.ai SDK (ibm-watsonx-ai)...
python -c "import ibm_watsonx_ai" >nul 2>&1
if errorlevel 1 (
    echo [INFO] IBM watsonx.ai SDK not found.
    echo        To enable IBM Granite LLM enhancement, run:
    echo          pip install ibm-watsonx-ai
    echo        Then set these environment variables:
    echo          set IBM_CLOUD_API_KEY=^<your-api-key^>
    echo          set WATSONX_PROJECT_ID=^<your-project-id^>
    echo        The agent runs fine without these – it uses local TF-IDF mode.
) else (
    echo [OK] IBM watsonx.ai SDK is installed.
    if "%IBM_CLOUD_API_KEY%"=="" (
        echo [WARN] IBM_CLOUD_API_KEY not set – running in local TF-IDF mode.
    ) else (
        echo [OK] IBM_CLOUD_API_KEY is set.
    )
    if "%WATSONX_PROJECT_ID%"=="" (
        echo [WARN] WATSONX_PROJECT_ID not set – running in local TF-IDF mode.
    ) else (
        echo [OK] WATSONX_PROJECT_ID is set.
    )
)

REM ── Step 4: Launch the agent ──────────────────────────────────────────────
echo.
echo ============================================================
echo   Starting EvidenceGuard AI on http://127.0.0.1:5000
echo   Open your browser to: http://127.0.0.1:5000
echo   Press CTRL+C to stop the server.
echo ============================================================
echo.

python backend/app.py

REM ── If server exits ───────────────────────────────────────────────────────
echo.
echo [INFO] EvidenceGuard AI server has stopped.
pause
