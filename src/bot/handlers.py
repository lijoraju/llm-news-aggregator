from telegram import Update
from telegram.ext import ContextTypes
from sentence_transformers import SentenceTransformer
import faiss, json
import numpy as np
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.user_profiles import (set_user_interests, get_user_interests, remove_user_preferences, 
                               SUPPORTED_CATEGORIES, load_profiles)
# from bot.initializer import initialize_pipeline

def load_model_and_data():
    # Ensure FAISS index and metadata are present
    # initialize_pipeline()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    faiss.omp_set_num_threads(1)
    index = faiss.read_index("data/processed/articles_faiss.index")
    with open("data/processed/article_metadata.json", "r") as f:
        articles = json.load(f)
    return model, index, articles

# Lazy loading for efficiency and testability
_model, _index, _articles = None, None, None

def get_resources():
    global _model, _index, _articles
    if _model is None or _index is None or _articles is None:
        _model, _index, _articles = load_model_and_data()
    return _model, _index, _articles

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    model, index, articles = get_resources()
    user_query = update.message.text.strip()
    user_id = update.effective_user.id
    interests = get_user_interests(user_id)

    query_vec = model.encode([user_query])
    D, I = index.search(np.array(query_vec).astype("float32"), k=10)

    reply = f"🧠 *Results for:* _{user_query}_\n\n"
    results = 0

    if not interests:
        reply += "_(No preferences set – showing top articles)_\nUse /setpreferences to personalize.\n\n"

    for idx in I[0]:
        article = articles[idx]
        category = article.get("category", "")
        title = article.get("title", "Untitled")
        summary = article.get("summary", "")
        url = article.get("url", "")

        if not interests or any(interest.lower() in category.lower() for interest in interests):
            reply += f"📌 *{title}*\n"
            if category:
                reply += f"🏷️ Category: `{category}`\n"
            if url:
                reply += f"🔗 [Read Full Article]({url})\n"
            reply += f"✂️ *Summary:* {summary}\n\n"
            results += 1

        if results >= 3:
            break

    if results == 0:
        reply += "⚠️ No results matched your preferences."

    await update.message.reply_markdown(reply[:4096])

async def set_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Please provide a comma-separated list of interests.\nExample:\n`/setpreferences Technology, AI`",
            parse_mode="Markdown"
        )
        return

    interests = [i.strip() for i in text.split(",") if i.strip()]
    invalid = [cat for cat in interests if cat not in SUPPORTED_CATEGORIES]

    if invalid:
        await update.message.reply_text(
            f"❌ Invalid categories: {', '.join(invalid)}\n\n✅ Allowed categories are:\n" +
            ", ".join(SUPPORTED_CATEGORIES)
        )
        return
    
    set_user_interests(user_id, interests)

    await update.message.reply_text(f"✅ Preferences saved: {', '.join(interests)}")

async def show_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    interests = get_user_interests(user_id)
    if not interests:
        await update.message.reply_text("You haven't set any preferences yet. Use /setpreferences to define them.")
    else:
        await update.message.reply_text(f"📌 Your preferences: {', '.join(interests)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 *Welcome to SmartNews Bot!*\n\n"
        "Here's what I can do:\n"
        "• Send me a message like `AI in healthcare`\n"
        "• I’ll send you relevant summaries from recent news articles\n\n"
        "📌 *Available Commands:*\n"
        "`/setpreferences Technology, Health` – Set your preferred categories\n"
        "`/preferences` – View your current preferences\n"
        "`/removepreferences` – Clear your preferences\n"
        "`/help` – Show this help message\n\n"
        "✅ *Supported Categories:*\n"
        "Technology, Business, Politics, Sports, Health, Science, Entertainment, Stock Market"
    )

    await update.message.reply_markdown(msg)

async def remove_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    success = remove_user_preferences(user_id)

    if success:
        await update.message.reply_text("✅ Your preferences have been removed. You can set new ones with /setpreferences.")
    else:
        await update.message.reply_text("ℹ️ You don’t have any preferences set yet.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = (
        f"👋 Hi {user.first_name or 'there'}!\n\n"
        "Welcome to *SmartNews Bot* – your personalized LLM-powered news assistant.\n\n"
        "You can:\n"
        "• Send me a message like `AI in finance`\n"
        "• Set preferences for the type of news you want\n\n"
        "⚙️ Use the buttons below or `/help` for all commands."
    )

    prefs = load_profiles()
    user_id_str = str(user.id)

    keyboard = []
    if user_id_str not in prefs:
        keyboard = [[InlineKeyboardButton("Set Preferences", callback_data="set_preferences")]]

    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
