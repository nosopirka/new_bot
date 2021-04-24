import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler

import settings


token = [
    settings.API_KEY
]
TOKEN = token[0]

PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}

logging.basicConfig(filename="bot.log", level=logging.INFO)


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def hp(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def main():
    updater = Updater(TOKEN, use_context=True,
                      request_kwargs=PROXY)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", hp))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()