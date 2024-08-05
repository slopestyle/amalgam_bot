from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from flask import Flask, request
import os

# Initialize Flask app and Telegram updater
app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_TOKEN')
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
        ],
        [
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    response_text = {
        '1': 'You pressed Button 1!',
        '2': 'You pressed Button 2!',
        '3': 'You pressed Button 3!',
        '4': 'You pressed Button 4!',
    }

    # Respond to the button press
    query.edit_message_text(text=response_text[query.data])

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, updater.bot)
    dispatcher.process_update(update)
    return 'ok'

# Handler function for Vercel
def handler(request):
    with app.request_context(request):
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run()
