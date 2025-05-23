from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    filters
)
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bot.handlers import handle_message, set_preferences, show_preferences, help_command, remove_preferences

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
    app.add_handler(CommandHandler("removepreferences", remove_preferences))

def run_bot():
    bot_token = load_bot_token()
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in environment variables.")
        return
    app = build_application(bot_token)
    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()