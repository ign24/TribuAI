# TribuAI Backend

Python backend for the TribuAI Cultural Intelligence Engine using LangGraph and Qloo API.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the API server
python -m uvicorn app.main:app --reload --port 8000

# Or run in development mode
python run_demo.py
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── langgraph_config.py  # LangGraph workflow
│   ├── qloo_client.py       # Qloo API client
│   ├── utils.py             # Utility functions
│   └── chains/              # LLM chains
├── data/                    # Sample data and mock responses
├── logs/                    # Application logs
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── run_demo.py             # Demo script
```

## 🔧 API Endpoints

### POST /api/process
Process user input and return cultural analysis.

**Request:**
```json
{
  "user_input": "I love indie rock, street art, and sustainable fashion"
}
```

**Response:**
```json
{
  "cultural_profile": {
    "identity": "Urban Creative Minimalist",
    "music": ["indie rock", "electronic"],
    "style": ["minimalist", "sustainable"]
  },
  "recommendations": {
    "brands": ["Patagonia", "Aesop", "Supreme"],
    "places": ["Berlin", "Tokyo", "Portland"],
    "audiences": ["creative professionals"]
  },
  "matching": {
    "suggested_match": "Sofia",
    "match_percentage": 83
  }
}
```

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **LangGraph** - Workflow orchestration
- **OpenAI GPT-4** - LLM for cultural analysis
- **Qloo API** - Cultural intelligence data
- **Pydantic** - Data validation
- **Loguru** - Logging

## 🔑 Environment Variables

```env
OPENAI_API_KEY=your_openai_key
X-Api-Key=your_qloo_api_key
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python test_tribuai.py
```

## 📊 Monitoring

- Logs are stored in `logs/tribuai.log`
- Application metrics available via `/health` endpoint
- Error handling with detailed logging

## 🚀 Deployment

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📄 License

MIT License - see LICENSE file for details. 