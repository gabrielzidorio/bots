from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, BaseHandler

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

app = ApplicationBuilder().token("7275427469:AAFJ4sBkEZ-d0yPeQg1ZMghIVhhEWzdHX4U").build()
app.add_handler(CommandHandler("hello", hello))
app.run_polling()