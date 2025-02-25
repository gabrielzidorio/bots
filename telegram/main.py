import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
sys.path.append('c:/users/zidorio/appdata/local/programs/python/python313/lib/site-packages')
API_KEY = '7275427469:AAFJ4sBkEZ-d0yPeQg1ZMghIVhhEWzdHX4U'
EXCHANGE_RATE_API_URL = 'https://api.exchangerate-api.com/v4/latest/'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou um bot que converte Real para Dólar e vice-versa. Use /convert <valor> <moeda de origem> <moeda de destino>')

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        amount = float(context.args[0])
        currency_src = context.args[1].upper()
        currency_dst = context.args[2].upper()
        if currency_src or currency_dst not in ['USD', 'BRL']:
            raise ValueError('Moeda não suportada.')

        response = requests.get(EXCHANGE_RATE_API_URL + 'BRL')
        data = response.json()
        rate = data['rates']['USD'] if currency == 'BRL' else 1 / data['rates']['USD']
        converted_amount = amount * rate
        await update.message.reply_text(f'{amount} {currency} é igual a {converted_amount:.2f} {"USD" if currency == "BRL" else "BRL"}.')

    except (IndexError, ValueError):
        await update.message.reply_text('Uso: /convert <valor> <moeda> (USD ou BRL)')

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = [
        '/start - Inicia o bot',
        '/convert <valor> <moeda> - Converte o valor de uma moeda para outra (USD ou BRL)',
        '/menu - Mostra este menu de ajuda'
    ]
    await update.message.reply_text('\n'.join(commands))

if __name__ == '__main__':
    app = ApplicationBuilder().token(API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("menu", menu))

    app.run_polling()