# 📰 LLM-Powered Personalized News Aggregator

A full-stack machine learning pipeline that fetches real-time news, summarizes it using LLMs, classifies articles into user-defined categories, and delivers personalized results via a Telegram bot. Built to showcase real-world LLM integration, automation, and cloud deployment — all using open-source tools and free-tier infrastructure.

---

## 🚀 Features

- 🔍 Fetches top news headlines using [NewsAPI](https://newsapi.org/)
- 📰 Extracts full article content with `newspaper3k`
- 🧼 Cleans and filters content using custom preprocessing
- 🧠 Summarizes using `facebook/bart-large-cnn` from HuggingFace Transformers
- 🏷️ Categorizes using zero-shot classification (`facebook/bart-large-mnli`)
- 🔎 Embeds summaries via MiniLM + stores in FAISS for efficient similarity search
- 🤖 Telegram bot delivers relevant news based on user preferences
- 🔁 Automated pipeline via GitHub Actions and cron
- ☁️ Deployed 24/7 using AWS EC2 (Free Tier)

---

## 🧠 Tech Stack

- Python, Conda, GitHub Actions
- HuggingFace Transformers (BART, MNLI)
- FAISS, SentenceTransformers
- NewsAPI, newspaper3k
- python-telegram-bot
- AWS EC2 (Free Tier)

---

## 📁 Project Structure
```
llm-news-aggregator/
├── src/
│ ├── bot/ # Telegram bot logic
│ ├── scraping/ # NewsAPI and fulltext extraction
│ ├── summarization/ # LLM-based summarization
│ ├── categorization/ # Zero-shot classification
│ ├── embedding/ # FAISS embeddings and search
│ ├── pipeline/ # refresh_pipeline.py entry point
│ ├── preprocessing/ # Text normalization
├── data/
│ └── processed/ # Auto-generated: index + metadata
├── notebooks/ # Colab/Local test notebooks
├── .github/workflows/ # GitHub Actions automation
├── environment.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/lijoraju/llm-news-aggregator.git
cd llm-news-aggregator

# Create environment
conda env create -f environment.yml
conda activate llm-news

# OR
python -m pip install --upgrade pip
pip install -r requirements.txt

# Add your API keys
cp .env.example .env
# Then edit .env and set:
# TELEGRAM_BOT_TOKEN=your_bot_token
# NEWS_API_KEY=your_newsapi_key

# Run the refresh pipeline
python src/pipeline/refresh_pipeline.py
```
## 💬 Telegram Bot Commands

```bash
# Start the bot (in tmux if on EC2)
python src/bot/telegram_bot.py

/start             → Welcome message
/help              → List of commands
/setpreferences    → Set preferred news categories
/preferences       → Show current preferences
/removepreferences → Remove saved preferences

```

## ✅ Supported categories:
Technology, Business, Politics, Sports, Health, Science, Entertainment, Stock Market

## 🔁 Refresh Automation Architecture
```
GitHub Actions (every 6 hours):
  └── Runs refresh_pipeline.py:
        ├── Scrapes fresh news
        ├── Summarizes via BART
        ├── Classifies via MNLI
        ├── Embeds via MiniLM
        └── Uploads FAISS index + metadata to EC2 via SCP

EC2 (tmux):
  └── Telegram bot runs continuously
      └── Uses updated index + metadata to serve live user queries
```

## 📌 Future Enhancements
 - Support user-specific long-term preferences
 - Summarize via faster LLMs (DistilBART, Pegasus)
 - Support news articles in regional langauges

## 📝 Credits
Developed by [Lijo Raju](https://www.linkedin.com/in/lijoraju/)

This project was built as a personal portfolio showcase to demonstrate:

- LLM pipeline design
- MLOps automation
- Cloud deployment
- Real-world user interaction

## 📜 License

This project is licensed under the MIT License.
