from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

import logging
from pymystem3 import Mystem

import datetime

from echo.config import TG_TOKEN
from echo.CountryNamesCurrencies import countries
from echo.CountryNamesCurrencies import currencies
from apis.CbBank import CbBank
from apis.Myfin import Myfin
from apis.Myfin import ParserError
from apis.CbBank import ParserErrorXML


# Функция для получения сообщения без окончаний
def get_message_without_endings(message: str):
    m = Mystem()
    lemmas = m.lemmatize(message)
    return ''.join(lemmas).lower()


# Функция старт бота
def do_start(bot: Bot, update: Update):
    logging.info('Вызов метода start')
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Напиши мне что-нибудь",
    )


# Функция help бота
def do_help(bot: Bot, update: Update):
    logging.info('Вызов метода help')
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Это бот\n\n"
             "Введите предложение, в котором есть город и валюта (доллар, евро ...), чтобы узнать курс\n\n"
             "Чтобы узнать курс в ЦБ, напишите /cb *Дата в формате день.месяц.год*\n\n"
             "Чтобы узнать какие города поддерживаются, напишите /countries\n\n"
             "Поддерживаются валюты: доллар, евро, фунт, иена, юань(не поддерживается в ЦБ)\n\n"
             "Также я отвечу повотором на любое твое сообщение",
    )


# Получить информацию с ЦБ по дате
def do_cb(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = update.message.text

    text_split = text.split(' ')
    date_text = text_split[1].split('.')
    day = date_text[0]
    month = date_text[1]
    year = date_text[2]

    try:
        date = datetime.date(int(year), int(month), int(day))
        text = 'Центробанк\n' + f'{date.day}.{date.month}.{date.year}\n'

        bank = CbBank(date)

        rate_usd = bank.get_rates_usd()
        rate_eur = bank.get_rates_eur()
        rate_gbp = bank.get_rates_gbp()
        rate_jpy = bank.get_rates_jpy()
        bot.send_message(
            chat_id=chat_id,
            text=text + f'{rate_usd.name} = {rate_usd.rate}\n' +
                 f'{rate_eur.name} = {rate_eur.rate}\n' +
                 f'{rate_gbp.name} = {rate_gbp.rate}\n' +
                 f'{rate_jpy.name} = {rate_jpy.rate}'
        )
    except ParserErrorXML:
        logging.info("Parser error")
        bot.send_message(
            chat_id=chat_id,
            text='Произошла неизвестная ошибка парсера'
        )
    except KeyError:
        logging.info("Invalid key")
        bot.send_message(
            chat_id=chat_id,
            text='Вы ввели невалидную дату'
        )
    except ValueError:
        logging.info("Value error")
        bot.send_message(
            chat_id=chat_id,
            text='Вы ввели невалидную дату'
        )


# Получить города
def do_countries(bot: Bot, update: Update):
    text = ''
    for country in countries.keys():
        text = text + country + '\n'
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text
    )


# Функция echo(повтор сообщений) бота и получения курса с Myfin
def do_echo_get_curr(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = update.message.text

    bot.send_message(
        chat_id=chat_id,
        text=text,
    )

    text_without_endings = get_message_without_endings(text)
    for currency_key, currency_value in currencies.items():
        if text_without_endings.find(currency_key.lower()) > -1:
            for country_key, country_value in countries.items():
                if text_without_endings.find(country_key.lower()) > -1:
                    try:
                        text_currency_country = currency_key + '\n' + 'г.' + country_key + '\n\n'
                        text = text_currency_country
                        banks = Myfin(country_value, currency_value)
                        banks_rates = banks.get_rate()

                        if len(banks_rates) >= 5:
                            banks_rates = banks_rates[0:5]
                            for bank in banks_rates:
                                text_bank = bank.bank_name + '\n' + bank.rate_buy + '\n' + bank.rate_sell + '\n\n'
                                text = text + text_bank
                        else:
                            for bank in banks_rates:
                                text_bank = bank.bank_name + '\n' + bank.rate_buy + '\n' + bank.rate_sell + '\n\n'
                                text = text + text_bank
                        bot.send_message(
                            chat_id=chat_id,
                            text=text
                        )
                        break
                    except ParserError:
                        logging.info('Parser error')
                        bot.send_message(
                            chat_id=chat_id,
                            text='Произошла ошибка доступа к сайту'
                        )
                    except AttributeError:
                        logging.info('Invalid attribute')
                        bot.send_message(
                            chat_id=chat_id,
                            text='Произошла ошибка поиска атрибута'
                        )
            break


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
    countries_handler = CommandHandler("countries", do_countries)
    cb_handler = CommandHandler("cb", do_cb)
    message_handler = MessageHandler(Filters.text, do_echo_get_curr)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(countries_handler)
    updater.dispatcher.add_handler(cb_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
