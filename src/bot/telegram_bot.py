from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    filters
)
from dotenv import load_dotenv
import os
from bot.handlers import handle_message, set_preferences, show_preferences, help_command

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("setpreferences", set_preferences))
    app.add_handler(CommandHandler("preferences", show_preferences))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("help", help_command))

    print("🤖 Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()