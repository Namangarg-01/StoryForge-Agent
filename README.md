# Content Generation MCP Server

An MCP (Model Context Protocol) server that combines real-time web search with local LLM generation for content creation.

## Features

- 🔍 Real-time web search using Tavily API
- 🤖 Local LLM generation using Ollama (phi3)
- 📝 Generate research summaries
- 🎬 Create video scripts from research

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Tavily API key ([Get one here](https://tavily.com/))

## Quick Start

### Option 1: Automatic Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

**Windows:**
```cmd
setup.bat
run.bat
```

### Option 2: Manual Setup

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd content-generation-mcp
```

2. **Create virtual environment**
```bash
   python -m venv venv
   
   # Activate it:
   # Linux/Mac:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
   cp .env.example .env
   # Edit .env and add your TAVILY_API_KEY
```

5. **Start Ollama and pull the model**
```bash
   # In a separate terminal:
   ollama serve
   
   # Pull the phi3 model:
   ollama pull phi3
```

6. **Run the server**
```bash
   python server.py
```

## Configuration

Edit `.env` file:
```env
TAVILY_API_KEY=your_actual_api_key_here
OLLAMA_MODEL_INFO=phi3
OLLAMA_MODEL_SCRIPT=phi3
```

## Usage

Once the server is running, you can use the following tools:

### 1. Get Real-time Information
```python
get_realtime_info(query="latest AI developments")
```

### 2. Generate Video Script
```python
generate_video_script(info_text="Your research summary here")
```

## Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running:
curl http://localhost:11434/api/tags

# If not, start it:
ollama serve
```

### Model Not Found
```bash
# Pull the required model:
ollama pull phi3

# List available models:
ollama list
```

### Tavily API Error
- Verify your API key in `.env`
- Check if you have API credits at [tavily.com](https://tavily.com/)

## Development

### Project Structure
```
content-generation-mcp/
├── server.py          # Main MCP server
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (not in git)
└── README.md         # This file
```

### Running Tests
```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/repo/issues)
- 📖 Docs: [Full Documentation](https://your-docs-site.com)