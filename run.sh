#!/bin/bash

echo "🚀 Starting Content Generation MCP Server..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "📝 Please copy .env.example to .env and add your API keys"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "⚠️  Ollama is not running"
    echo "Please start Ollama in another terminal: ollama serve"
    echo ""
    read -p "Press Enter when Ollama is running..."
fi

# Run the server
echo "✓ Starting server..."
python server.py