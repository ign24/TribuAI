# 🌍 TribuAI - Cultural Intelligence Engine

TribuAI is a modern web application that uses AI to analyze cultural preferences and connect people with similar cultural identities. It uses **LangGraph for intelligent conversation orchestration** and **Qloo API for 100% real cultural data**, creating a powerful synergy between LLM capabilities and cultural intelligence.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API Keys (OpenAI, Qloo)

### 1. Clone and setup
```bash
git clone <your-repo-url>
cd TribuAI
```

### 2. Backend Setup
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your keys:
# OPENAI_API_KEY=your_openai_key
# X-Api-Key=your_qloo_api_key
```

### 3. Frontend Setup
```bash
# Install Node.js dependencies
cd frontend
npm install
```

### 4. Start development servers
```bash
# From project root
python start_dev.py
```
This starts both servers:
- **Frontend**: http://localhost:3000 (or http://localhost:5173)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
TribuAI/
├── backend/                 # Python FastAPI Backend
│   ├── app/                # Application code
│   │   ├── api.py          # FastAPI routes
│   │   ├── main.py         # Core TribuAI logic
│   │   ├── langgraph_config.py  # LangGraph conversation flow
│   │   ├── qloo_client.py  # Simplified Qloo API client
│   │   └── utils.py        # Utilities
│   ├── data/               # Sample data
│   ├── logs/               # Logs
│   ├── requirements.txt    # Python dependencies
│   └── run_demo.py         # Demo script
├── frontend/               # Vue 3 + Vite Frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Main views
│   │   ├── composables/    # Reusable logic
│   │   │   ├── useApi.ts   # API client
│   │   │   └── useConversation.ts  # Conversation system
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── config/         # API configuration
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── start_dev.py           # Development script
└── README.md              # This file
```

## 🔄 Data Flow (LangGraph + Qloo Integration)

### Intelligent Conversation System

1. **LangGraph orchestrates conversation** with natural language processing:
   - 🎵 Music: "What kind of music do you love?"
   - 🎨 Art: "What art forms inspire you?"
   - 👗 Fashion: "How would you describe your style?"
   - 💎 Values: "What values are most important to you?"
   - 🌍 Places: "What places or environments do you love?"
   - 👥 Communities: "What communities do you identify with?"

2. **User responds naturally** in Spanish or English

3. **LangGraph extracts entities** intelligently using LLM capabilities

4. **When profile is complete** (minimum 3 categories), LangGraph sends complete cultural profile to backend

5. **Backend processes** using simplified Qloo API requests for 100% real data

6. **Frontend displays** cultural profile, real recommendations, and matching

### API Endpoints

#### POST /api/process-profile (Main)
Processes a complete cultural profile with real Qloo data.

**Request:**
```json
{
  "music": ["jazz", "electronic"],
  "art": ["cinema", "photography"],
  "fashion": ["minimalist", "streetwear"],
  "values": ["authenticity", "sustainability"],
  "places": ["cities", "cafes"],
  "audiences": ["creatives", "entrepreneurs"]
}
```

**Response:**
```json
{
  "cultural_profile": {
    "identity": "Creative Cultural Explorer",
    "description": "Someone who appreciates both music and visual arts, with a keen eye for style and cultural expression.",
    "music": ["jazz", "electronic"],
    "style": ["minimalist", "streetwear"]
  },
  "recommendations": {
    "brands": [
      {
        "name": "Real Brand from Qloo",
        "entity_id": "real_qloo_id",
        "description": "Real description from Qloo API",
        "image": "https://real-image-url.com", // always present or replaced by a default icon in the UI
        "tags": ["real", "tags", "from", "qloo"]
      }
      // ... up to 3 filtered, high-quality brands
    ],
    "places": [
      {
        "name": "Real Place from Qloo",
        "entity_id": "real_qloo_id",
        "description": "Real description from Qloo API",
        "image": "https://real-image-url.com", // always present or replaced by a default icon in the UI
        "tags": ["real", "tags", "from", "qloo"]
      }
      // ... up to 3 filtered, high-quality places
    ]
  },
  "matching": {
    "affinity_percentage": 90,
    "shared_interests": ["jazz", "cinema", "minimalist"],
    "audience_cluster": "Cultural Enthusiast"
  }
}
```

#### POST /api/process (LangGraph Flow)
Maintains LangGraph conversation orchestration for complex interactions.

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern web framework
- **LangGraph** - Intelligent conversation orchestration
- **OpenAI GPT-4** - LLM for cultural analysis and entity extraction
- **Qloo API** - 100% real cultural intelligence data
- **Pydantic** - Data validation
- **Loguru** - Logging

### Frontend
- **Vue 3** - Progressive framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility CSS
- **Pinia** - State management
- **Vue Router** - Routing
- **TypeScript** - Static typing

## 🎯 Key Features

### LangGraph Conversation System
- **Intelligent conversation orchestration** using LangGraph
- **Natural language processing** for entity extraction
- **Multi-turn conversations** with context awareness
- **Spanish and English support**

### Real Data Integration
- **100% real data** from Qloo API
- **Simplified API requests** for reliability
- **Cultural intelligence** with actual recommendations
- **No mock data fallback** - only real results

### Cultural Processing
- **Direct analysis** of cultural profiles
- **Personalized recommendations** for brands and places
- **Cultural matching** with affinity percentages
- **Real cultural intelligence** data
- **Filtered & prioritized recommendations**: backend removes duplicates, excludes generic names (like 'Brand' or 'Place'), prioritizes those with description or image, and limits to 3 high-quality results per section.

### UI/UX
- **Modern interface** with responsive design
- **Smooth animations** and transitions
- **Debug mode** for development
- **Detailed logging** in console
- **Visual recommendations**: frontend always shows an image or a default icon for each brand/place, ensuring every card is visually appealing even if Qloo data is incomplete.

## 🏆 Hackathon Strategy

### Intelligent & Thoughtful use of LLMs
- **LangGraph orchestration** for complex conversation flows
- **LLM-powered entity extraction** from natural language
- **Context-aware recommendations** based on cultural profiles

### Integration with Qloo's API
- **Simplified but effective** use of Qloo API
- **Real cultural data** for recommendations
- **Cross-domain affinities** through actual API responses

### Technical Implementation
- **Solid code architecture** with FastAPI + LangGraph
- **Reliable API integration** with proper error handling
- **Modern frontend** with Vue 3 + TypeScript

### Originality & Creativity
- **Cultural intelligence chatbot** with natural conversation
- **Cross-domain recommendations** (music + places + brands)
- **Personalized cultural matching** system

### Real-World Application
- **Cultural discovery platform** for users
- **Recommendation engine** for brands and places
- **Community building** through cultural affinities

## 🖥️ Development and Troubleshooting

### Logs and Debug
- **Frontend logs:** Open browser console to see detailed logs
- **Backend logs:** Check logs in `backend/logs/`
- **LangGraph traces:** Detailed conversation flow logging

### Common Issues
- **Qloo API limits:** System uses simplified requests for reliability
- **Conversation flow:** LangGraph handles complex state management
- **Entity extraction:** LLM-powered extraction from natural language

### Testing
```bash
# Backend
cd backend
python test_tribuai.py

# Frontend
cd frontend
npm run dev

# API Testing
curl -X POST http://localhost:8000/api/process-profile \
  -H "Content-Type: application/json" \
  -d '{"music":["jazz"],"art":["cinema"],"fashion":["minimalist"]}'
```

## 🚀 Deployment

### Backend
```bash
cd backend
pip install gunicorn
gunicorn app.api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd frontend
npm run build
# Deploy dist/ folder to your hosting
```

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Make a pull request

## 📄 License

MIT License - see LICENSE

## 🙏 Acknowledgments

- **Qloo API** for cultural intelligence data
- **OpenAI** for GPT-4
- **LangGraph** for intelligent conversation orchestration
- **Vue.js** for the framework

---

**TribuAI** - Connecting cultures with AI 🤖🌍
