from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import faiss, json, os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

def run_bot():
    load_dotenv()
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    faiss.omp_set_num_threads(1)
    index = faiss.read_index("data/processed/articles_faiss.index")
    with open("data/processed/article_metadata.json", "r") as f:
        articles = json.load(f)
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_query = update.message.text.strip()
        query_vec = model.encode([user_query])
        D, I = index.search(np.array(query_vec).astype("float32"), k=3)

        reply = f"🧠 *Results for:* _{user_query}_\n\n"
        for idx in I[0]:
            article = articles[idx]
            reply += f"📌 *{article['title']}*\n🏷️ {article['category']}\n✂️ {article['summary']}\n\n"
        
        await update.message.reply_markdown(reply[:4096])

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    run_bot()