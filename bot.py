from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')

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

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

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

    query.edit_message_text(text=page_content[query.data], reply_markup=reply_markup, parse_mode='Markdown')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
