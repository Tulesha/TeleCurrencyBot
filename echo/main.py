import telebot
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

bot = telebot.TeleBot(TG_TOKEN)


# Функция для получения сообщения без окончаний
def get_message_without_endings(message: str):
    m = Mystem()
    lemmas = m.lemmatize(message)
    return ''.join(lemmas).lower()


# Функция старт бота
@bot.message_handler(commands=['start'])
def do_start(message):
    logging.info('Вызов метода start')
    bot.send_message(message.chat.id, 'Привет! Я бот и мне нормально')


# Функция help бота
@bot.message_handler(commands=['help'])
def do_help(message):
    logging.info('Вызов метода help')
    bot.send_message(
        message.chat.id,
        "Это бот\n\n" +
        "Введите предложение, в котором есть город и валюта (доллар, евро ...), чтобы узнать курс\n\n" +
        "Чтобы узнать курс в ЦБ, напишите /cb *Дата в формате день.месяц.год*\n\n" +
        "Чтобы узнать какие города поддерживаются, напишите /countries\n\n" +
        "Поддерживаются валюты: доллар, евро, фунт, иена, юань(не поддерживается в ЦБ)\n\n" +
        "Также я отвечу повотором на любое твое сообщение",
    )


# Получить города
@bot.message_handler(commands=['countries'])
def do_countries(message):
    logging.info('Вызов метода do_countries')
    text = ''
    for country in countries.keys():
        text = text + country + '\n'
    bot.send_message(
        message.chat.id,
        text
    )


# Получить информацию с ЦБ по дате
@bot.message_handler(commands=['cb'])
def do_cb(message):
    logging.info('Вызов метода do_cb')
    chat_id = message.chat.id
    text = message.text

    try:
        text_split = text.split(' ')
        date_text = text_split[1].split('.')
        day = date_text[0]
        month = date_text[1]
        year = date_text[2]

        date = datetime.date(int(year), int(month), int(day))
        text = 'Центробанк\n' + f'{date.day}.{date.month}.{date.year}\n'

        bank = CbBank(date)

        rate_usd = bank.get_rates_usd()
        rate_eur = bank.get_rates_eur()
        rate_gbp = bank.get_rates_gbp()
        rate_jpy = bank.get_rates_jpy()
        bot.send_message(
            chat_id,
            text + f'{rate_usd.name} = {rate_usd.rate}\n' +
            f'{rate_eur.name} = {rate_eur.rate}\n' +
            f'{rate_gbp.name} = {rate_gbp.rate}\n' +
            f'{rate_jpy.name} = {rate_jpy.rate}'
        )
    except ParserErrorXML:
        logging.info("Parser error")
        bot.send_message(
            chat_id,
            'Произошла неизвестная ошибка парсера'
        )
    except KeyError:
        logging.info("Invalid key")
        bot.send_message(
            chat_id,
            'Вы ввели невалидную дату'
        )
    except ValueError:
        logging.info("Value error")
        bot.send_message(
            chat_id,
            'Вы ввели невалидную дату'
        )
    except IndexError:
        logging.info("Index error")
        bot.send_message(
            chat_id,
            'Введите валидную дату'
        )


# Получение валюты с Myfin
def get_curr(chat_id, text_without_endings: str):
    flag = False
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
                            chat_id,
                            text
                        )
                        flag = True
                        break
                    except ParserError:
                        logging.info('Parser error')
                        bot.send_message(
                            chat_id,
                            'Произошла ошибка доступа к сайту'
                        )
                    except AttributeError:
                        logging.info('Invalid attribute')
                        bot.send_message(
                            chat_id,
                            'Произошла ошибка поиска атрибута'
                        )
            break
    if not flag:
        bot.send_message(
            chat_id,
            'Я вас не понимаю. Я могу показать валюту в нужном вам городе'
        )


# Функция echo(повтор сообщений) бота и получения курса с Myfin
@bot.message_handler(content_types=['text'])
def do_echo_get_curr(message):
    logging.info('Вызов метода do_echo_get_curr')
    chat_id = message.chat.id

    text_without_endings = get_message_without_endings(message.text)

    if message.chat.type == "private":
        bot.send_message(
            chat_id,
            'Секундочку...'
        )
        get_curr(chat_id, text_without_endings)

    elif message.chat.type == "group":
        if text_without_endings.find("@Currency_ITMO_bot".lower()) > -1:
            bot.send_message(
                chat_id,
                'Секундочку...'
            )
            get_curr(chat_id, text_without_endings)


@bot.message_handler(content_types=["sticker"])
def do_sticker(message):
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классный стикер'
        )


@bot.message_handler(content_types=["photo"])
def do_photo(message):
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классное фото'
        )


@bot.message_handler(content_types=["audio"])
def do_audio(message):
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классное аудио'
        )


@bot.message_handler(content_types=["document"])
def do_document(message):
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классный документ'
        )


bot.polling(none_stop=True, interval=0)
