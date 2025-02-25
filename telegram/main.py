import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
sys.path.append('c:/users/zidorio/appdata/local/programs/python/python313/lib/site-packages')
API_KEY = '7275427469:AAFJ4sBkEZ-d0yPeQg1ZMghIVhhEWzdHX4U'
EXCHANGE_RATE_API_URL = 'https://api.exchangerate-api.com/v4/latest/'

accept_currencies = {'USD - Dólar', 'BRL - Real Brasileiro', 'GPB - Libra Estrelina', 'EUR - Euro', 'ARS - Peso Argentino'}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou um bot que converte Real para Dólar e vice-versa. Use /menu e veja o que eu posso fazer por você!')
    
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        amount = float(context.args[0])
        currency_src = context.args[1].upper()
        currency_dst = context.args[2].upper()
        if currency_src or currency_dst not in accept_currencies:
            raise ValueError('Moeda não suportada.')
        elif currency_src == currency_dst:
            raise ValueError('As moedas de origem e destino devem ser diferentes.')
        
        response_src = requests.get(EXCHANGE_RATE_API_URL + currency_src)
        response_dst = requests.get(EXCHANGE_RATE_API_URL + currency_dst)
        
        if response_src < response_dst:
           data = response_src.json()
           rate = data['rates'][currency_dst]
           converted_amount = amount * rate 
           await update.message.reply_text(f'{amount} {currency_src} é igual a {converted_amount:.2f} {currency_dst}.')
        else:
            data = response_src.json()
            rate = data['rates'][currency_dst]
            converted_amount = amount / rate 
            await update.message.reply_text(f'{amount} {currency_src} é igual a {converted_amount:.2f} {currency_dst}.')        
#        response = requests.get(EXCHANGE_RATE_API_URL + 'BRL')
#        data = response.json()
#        rate = data['rates']['USD'] if currency_src == 'BRL' else 1 / data['rates']['USD']
#        converted_amount = amount * rate
#        await update.message.reply_text(f'{amount} {currency_src} é igual a {converted_amount:.2f} {"USD" if currency_dst == "BRL" else "BRL"}.')

    except (IndexError, ValueError):
        await update.message.reply_text('Uso: /convert <valor> <moeda> (USD ou BRL)')

async def currencies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('\n'.join(accept_currencies))

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands = [
        '/convert <valor> <moeda de origem> e <moeda de destino> - Converte o valor de uma moeda para outra',
        '/currencies - Mostra as moedas suportadas',
        '/menu - Mostra este menu de ajuda'
    ]
    await update.message.reply_text('\n'.join(commands))

if __name__ == '__main__':
    app = ApplicationBuilder().token(API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("currencies", currencies))
    app.add_handler(CommandHandler("menu", menu))

    app.run_polling()