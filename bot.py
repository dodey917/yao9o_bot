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

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Your Telegram ID for notifications

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User data storage (in-memory for simplicity)
user_data = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    
    # Initialize user data
    user_data[user_id] = {
        'completed_tasks': False,
        'sol_wallet': None
    }
    
    # Create task buttons
    keyboard = [
        [InlineKeyboardButton("✅ I Joined Channel", callback_data='joined_channel')],
        [InlineKeyboardButton("🐦 I Followed Twitter", callback_data='followed_twitter')],
        [InlineKeyboardButton("💰 Submit SOL Wallet", callback_data='submit_wallet')],
        [InlineKeyboardButton("🏆 Complete Airdrop", callback_data='complete_airdrop')]
    ]
    
    # Custom message with your links
    message = (
        f"👋 Welcome {user.first_name} to Mr. Michael's Airdrop!\n\n"
        "📋 To qualify:\n"
        "1. Join our channel: https://t.me/Yakstaschannel\n"
        "2. Join our group: https://t.me/yakstascapital\n"
        "3. Follow our Twitter: https://twitter.com/bigbangdist10\n"
        "4. Like our Facebook: https://www.facebook.com/bigbangdistribution\n\n"
        "Complete the steps and submit your SOL wallet address:"
    )
    
    update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    
    if data == 'joined_channel':
        query.answer("✅ Channel join recorded! Hope you didn't cheat!")
    elif data == 'followed_twitter':
        query.answer("✅ Twitter follow recorded! Hope you didn't cheat!")
    elif data == 'submit_wallet':
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Please send your Solana wallet address:"
        )
    elif data == 'complete_airdrop':
        check_completion(update, user_id)

def handle_wallet(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    wallet = update.message.text.strip()
    
    # Simple SOL address validation
    if len(wallet) < 32 or len(wallet) > 44:
        update.message.reply_text("❌ Invalid SOL address format. Please try again.")
        return
    
    # Store wallet (in memory)
    if user_id in user_data:
        user_data[user_id]['sol_wallet'] = wallet
    
    update.message.reply_text(
        "✅ Wallet received! Now click '🏆 Complete Airdrop' to finish."
    )

def check_completion(update: Update, user_id: int):
    query = update.callback_query
    
    # Get user status
    status = user_data.get(user_id, {})
    wallet = status.get('sol_wallet', '')
    
    # Custom congratulations message
    congrats_msg = (
        "🎉 *CONGRATULATIONS!*\n\n"
        "You passed Mr. Michael's Airdrop call!\n"
        f"100 SOL is on its way to your wallet:\n`{wallet}`\n\n"
        "⚠️ *Important Notes:*\n"
        "1. This is a TEST bot - no actual SOL will be sent\n"
        "2. Hope you didn't cheat the system!\n"
        "3. Thank you for participating!"
    )
    
    query.answer()
    query.edit_message_text(
        congrats_msg,
        parse_mode="Markdown"
    )
    
    # Send notification to admin
    try:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚨 New airdrop completion:\nUser: {query.from_user.username}\nWallet: {wallet}"
        )
    except Exception as e:
        logger.error(f"Admin notification failed: {e}")

def main():
    # Create the Updater
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_wallet))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
