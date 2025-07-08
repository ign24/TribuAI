# TribuAI

TribuAI is an AI-powered cultural intelligence engine that builds **personalized taste profiles** and **brand recommendations** based on your cultural identity. It uses **LLMs**, **LangGraph**, and the **Qloo Taste API** to understand who you are — not just what you like — and connects you with brands, communities, and experiences that resonate with your identity.

> ✨ "Because you're more than a user — you're a cultural signal."

---

## 🔍 What It Does

TribuAI helps users:
- 🧠 **Discover their cultural profile** through a personalized LLM-powered conversation
- 🎯 **Receive brand and experience recommendations** using real affinity data from Qloo
- 🌍 **Understand which audiences they belong to** (e.g., "Neo-minimalist Creatives", "Digital Nomads", "Latinx Queer Eclectics")
- 🤝 Optionally connect with users who share cultural affinity

---

## 💡 Use Case

Built for the [Qloo + GenAI Hackathon](https://www.qloo.com/), TribuAI demonstrates the power of **Taste AI** and **language models** to map identity, culture, and commerce.

Use cases include:
- Market-matching & audience segmentation
- Taste-based product recommendations
- Cultural profiling for lifestyle apps or travel tech
- Personalized brand discovery and community-building

---

## 🧠 How It Works

TribuAI is structured as a **graph of intelligent agents**, each performing a specific role in the pipeline:

User → LangGraph Flow → Qloo API → Cultural Profile → Recommendations → [Optional Matching] → Output

### 🔄 LangGraph Nodes:

| Node              | Description |
|-------------------|-------------|
| `intro`           | Introduction and explanation of the experience |
| `survey`          | Dynamic cultural questions powered by LLM |
| `llm_parser`      | Extracts structured entities, preferences and signals |
| `qloo_affinity`   | Queries Qloo's Taste API for audiences, brands, and cultural affinities |
| `profile_generator` | Assembles the user's cultural identity profile |
| `recommendations` | Curates personalized brands, locations and tags |
| `optional_match`  | Suggests culturally similar profiles (optional) |
| `end`             | Shows final output and allows restart/export |

---

## ⚙️ Tech Stack

| Component | Technology |
|----------|------------|
| Graph Flow | [LangGraph](https://www.langgraph.dev/) |
| LLMs | OpenAI GPT-4 |
| Cultural Intelligence API | [Qloo API](https://www.qloo.com/) |
| LangChain Tools | Custom parsing chain, memory, and prompt templates |
| UI (optional) | Streamlit (light demo), CLI for core testing |
| Environment | Python 3.11+, `.env` with API keys |

---

## 📁 Project Structure

tribuai/
├── app/
│ ├── main.py # Entry point and runner
│ ├── langgraph_config.py # Graph definition with all nodes
│ ├── chains/ # LangChain chains and tools
│ ├── prompts/ # Prompt templates
│ ├── qloo_client.py # API wrapper
│ └── utils.py # Helper functions
├── data/
│ ├── mock_inputs.json
│ ├── sample_profiles.json
├── docs/
│ ├── README.md
│ └── flowchart.png
├── .env
├── requirements.txt
└── run_demo.py

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/youruser/tribuai.git
cd tribuai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up API Keys

Create a .env file with the following:

```ini
OPENAI_API_KEY=your_key
X-Api-Key=your_key
```

### 4. Run the demo

```bash
python run_demo.py
```

Or launch a Streamlit demo:

```bash
streamlit run app/main.py
```

---

## 🧪 Examples

👤 User: "I love Japanese cinema, brutalist architecture, and old-school hip hop."

📈 Affinity Analysis:
- 🎵 Music: Nas, MF DOOM
- 🎨 Style: Minimal Streetwear
- 🏙️ Destinations: Tokyo, Berlin
- 👥 Audience: "Retro Aesthetics", "Urban Creatives"

💡 Brand Recommendations:
- Uniqlo, Supreme, Muji, BAPE

🤝 Suggested Match:
- Sofia, 28, Mexico City — similar cultural profile.

---

## ✨ Roadmap

- Add visualization dashboard (personas, profiles, maps)
- Fine-tune LangGraph edges for personalization
- Enable user profile export & social sharing
- Deploy to Hugging Face or Streamlit Cloud
- Prepare pitch deck + video for submission

---

## 🤝 Authors

Built by @ignacioz-ai for the GenAI Hackathon using cutting-edge LLM tech and cultural AI.

---

## 🏆 Hackathon Submission

Check out our full submission here

> "TribuAI doesn't classify you. It listens, understands… and connects you."
