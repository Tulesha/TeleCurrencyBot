from datetime import datetime

from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from echo.config import TG_TOKEN


# Функция старт бота
def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Напиши мне что-нибудь",
    )


# Функция help бота
def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Это бот\n\n"
             "Список доступных команд есть в меню\n\n"
             "Также я отвечу на любое сообщение",
    )


# Функция time(Время на сервере) бота
def do_time(bot: Bot, update: Update):
    now = datetime.now()
    text = "{}.{}.{} {}:{}:{}".format(now.day, now.month, now.year, now.hour, now.minute, now.second)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Дата и время на сервере: \n{}".format(text),
    )


# Функция echo(повтор сообщений) бота
def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = "Твой ID = {}\n\n{}".format(chat_id, update.message.text)

    bot.send_message(
        chat_id=chat_id,
        text=text,
    )


# Main
def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
