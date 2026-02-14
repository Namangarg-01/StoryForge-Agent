#!/bin/bash

echo "🚀 Setting up Content Generation MCP Server..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example if .env doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your TAVILY_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "✓ Ollama is running"
        
        # Pull phi3 model
        echo "📥 Pulling phi3 model..."
        ollama pull phi3
    else
        echo "⚠️  Ollama is not running. Please start it with: ollama serve"
    fi
else
    echo "❌ Ollama is not installed"
    echo "📖 Install from: https://ollama.ai/"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your TAVILY_API_KEY"
echo "2. Make sure Ollama is running: ollama serve"
echo "3. Run the server: ./run.sh"