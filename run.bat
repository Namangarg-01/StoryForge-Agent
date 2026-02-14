@echo off
echo 🚀 Starting Content Generation MCP Server...

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found. Run setup.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found
    echo 📝 Please copy .env.example to .env and add your API keys
    pause
    exit /b 1
)

REM Check if Ollama is running (simplified check)
echo ⚠️  Make sure Ollama is running in another terminal: ollama serve
echo.
pause

REM Run the server
echo ✓ Starting server...
python server.py

pause