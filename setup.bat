@echo off
echo 🚀 Setting up Content Generation MCP Server...

REM Check Python
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed
    echo 📖 Install from: https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy .env.example if .env doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your TAVILY_API_KEY
) else (
    echo ✓ .env file already exists
)

REM Check if Ollama is installed
where ollama >nul 2>nul
if %errorlevel% equ 0 (
    echo ✓ Ollama is installed
    
    REM Pull phi3 model
    echo 📥 Pulling phi3 model...
    ollama pull phi3
) else (
    echo ❌ Ollama is not installed
    echo 📖 Install from: https://ollama.ai/
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your TAVILY_API_KEY
echo 2. Make sure Ollama is running: ollama serve
echo 3. Run the server: run.bat

pause