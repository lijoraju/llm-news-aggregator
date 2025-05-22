from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    filters
)
from dotenv import load_dotenv
import sys
import os
from flask import Flask
import threading
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bot.handlers import handle_message, set_preferences, show_preferences, help_command

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "LLM Telegram Bot is running."

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

def load_bot_token():
    load_dotenv()
    return os.getenv("TELEGRAM_BOT_TOKEN")

def build_application(bot_token):
    app = ApplicationBuilder().token(bot_token).build()
    register_handlers(app)
    return app

def register_handlers(app):
    app.add_handler(CommandHandler("setpreferences", set_preferences))
    app.add_handler(CommandHandler("preferences", show_preferences))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("help", help_command))

def run_bot():
    bot_token = load_bot_token()
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables.")
        return
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = build_application(bot_token)
    print("🤖 Telegram bot is running...")
    app.run_polling(stop_signals=())

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()