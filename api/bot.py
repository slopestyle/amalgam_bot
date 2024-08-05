from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from flask import Flask, request
import os
import logging

TOKEN = os.getenv('TELEGRAM_TOKEN')
IMAGES = {
    'page_1': 'https://images.pexels.com/photos/1547813/pexels-photo-1547813.jpeg',
    'page_2': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Altja_j%C3%B5gi_Lahemaal.jpg/286px-Altja_j%C3%B5gi_Lahemaal.jpg',
    'page_3': 'https://assets.weforum.org/article/image/responsive_big_webp_0ZUBmNNVLRCfn3NdU55nQ00UF64m2ObtcDS0grx02fA.webp',
    'page_4': 'https://i.natgeofe.com/n/726708f7-f79d-47a5-ba03-711449823607/01-balance-of-nature.jpg?w=1280&h=853'
}

app = Flask(__name__)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Page 1", callback_data='page_1'),
            InlineKeyboardButton("Page 2", callback_data='page_2'),
        ],
        [
            InlineKeyboardButton("Page 3", callback_data='page_3'),
            InlineKeyboardButton("Page 4", callback_data='page_4'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a welcome message with the start button
    update.message.reply_text(
        'Welcome! Click the button below to start.',
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    page_content = {
        'page_1': 'This is Page 1. [Go back](start)',
        'page_2': 'This is Page 2. [Go back](start)',
        'page_3': 'This is Page 3. [Go back](start)',
        'page_4': 'This is Page 4. [Go back](start)',
    }

    keyboard = [[InlineKeyboardButton("Back to Home", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send image along with the text
    context.bot.send_photo(chat_id=query.message.chat_id, photo=IMAGES[query.data])
    query.edit_message_text(text=page_content[query.data], reply_markup=reply_markup, parse_mode='Markdown')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = Update.de_json(json_str, updater.bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run()
