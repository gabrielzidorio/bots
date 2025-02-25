import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.send_message(chat_id=update.effective_chat.id, text=f'Hello {update.effective_user.first_name}')
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

if __name__ == '__main__':
    app = ApplicationBuilder().token("7275427469:AAFJ4sBkEZ-d0yPeQg1ZMghIVhhEWzdHX4U").build()
    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)
    app.run_polling()
    