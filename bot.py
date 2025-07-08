import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

# Configuration with debugging
BOT_TOKEN = os.getenv("BOT_TOKEN", "DEFAULT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID", "DEFAULT_ADMIN")
PORT = int(os.getenv("PORT", 10000))

# Enable detailed logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Log environment variables at startup
logger.info(f"BOT_TOKEN: {'SET' if BOT_TOKEN != 'DEFAULT_TOKEN' else 'MISSING'}")
logger.info(f"ADMIN_ID: {'SET' if ADMIN_ID != 'DEFAULT_ADMIN' else 'MISSING'}")
logger.info(f"PORT: {PORT}")

# User data storage (in-memory)
user_data = {}

def start(update: Update, context: CallbackContext):
    # ... rest of your start function unchanged ...

def main():
    logger.info("Starting bot...")
    
    if BOT_TOKEN == "DEFAULT_TOKEN":
        logger.error("❌ MISSING BOT_TOKEN! Please set in environment variables")
        return
    
    try:
        updater = Updater(BOT_TOKEN)
        dp = updater.dispatcher

        # Add handlers
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CallbackQueryHandler(button_handler))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))
        
        # Health check command
        dp.add_handler(CommandHandler('status', 
            lambda u, c: u.message.reply_text("✅ Bot is online!"))
        
        # Render-specific setup
        if "RENDER" in os.environ:
            logger.info("Starting in WEBHOOK mode")
            updater.start_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=BOT_TOKEN,
                webhook_url=f"https://{os.getenv('RENDER_SERVICE_NAME')}.onrender.com/{BOT_TOKEN}"
            )
        else:
            logger.info("Starting in POLLING mode")
            updater.start_polling()
            
        logger.info("🤖 Bot is now running")
        updater.idle()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
