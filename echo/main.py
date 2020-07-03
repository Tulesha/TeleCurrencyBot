import re
import telebot
from datetime import datetime

from echo.config import TG_TOKEN
from echo.cityNamesCurrencies import cities
from echo.cityNamesCurrencies import currencies

from apis.cbBank import CbBank
from apis.cbBank import CentralBankError

from apis.Myfin import Myfin
from apis.Myfin import MyFinBankError

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def do_start(message):
    """
    Функция страта
    :param message: сообщение пользователя
    :return: сообщение о старте
    """
    bot.send_message(message.chat.id, 'Привет! Я бот и мне нормально')


@bot.message_handler(commands=['help'])
def do_help(message):
    """
    Функция помощи
    :param message: ссообщение от пользователя
    :return: сообщение о помощи
    """
    bot.send_message(
        message.chat.id,
        "Это бот\n\n" +
        "Введите предложение, в котором есть город и валюта (доллар, евро ...), чтобы узнать курс\n\n" +
        "Чтобы узнать курс в ЦБ, напишите /cb *Валюта на русском языке* *Дата в формате ДЕНЬ-МЕСЯЦ-ГОД*\n\n" +
        "Чтобы узнать какие города поддерживаются, напишите /cities\n\n" +
        "Поддерживаются валюты: доллар, евро, фунт, иена, юань(не поддерживается в ЦБ)\n\n" +
        "Также я отвечу повотором на любое твое сообщение",
    )


@bot.message_handler(commands=['cities'])
def do_cities(message):
    """
    Функция, выводящая на экран все поддерживаемые города
    :param message: сообщение от пользователя
    :return: информация о городах
    """
    text = ''
    for city in cities.keys():
        text = text + city + '\n'
    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(commands=['cb'])
def do_cb(message):
    """
    Функция, находящая курс валюты от текущей даты в ЦБ
    :param message: сообщение пользователя
    :return: информация о курсе за текующую дату
    """
    chat_id = message.chat.id
    try:
        text = str(message.text).lower()
        result = re.findall(r'доллар|евр|фунт|иен|', text)
        result += re.findall(r'\d*-\d*-\d*', text)
        result = list(filter(lambda a: a != '', result))

        if len(result) == 2:
            date_format = "%d-%m-%Y"
            date = datetime.strptime(result[1], date_format)

            text = 'Центробанк\n' + f'{date.strftime(date_format)}\n'
            bank = CbBank(date)

            if result[0] == 'доллар':
                rate_usd = bank.get_rates_usd()
                bot.send_message(
                    chat_id,
                    text + f'{rate_usd.name}\n{rate_usd.rate} руб.'
                )
            if result[0] == 'евр':
                rate_eur = bank.get_rates_eur()
                bot.send_message(
                    chat_id,
                    text + f'{rate_eur.name}\n{rate_eur.rate}руб.'
                )
            if result[0] == 'фунт':
                rate_gbp = bank.get_rates_gbp()
                bot.send_message(
                    chat_id,
                    text + f'{rate_gbp.name}\n{rate_gbp.rate}руб.'
                )
            if result[0] == 'иен':
                rate_jpy = bank.get_rates_jpy()
                bot.send_message(
                    chat_id,
                    text + f'{rate_jpy.name}\n{rate_jpy.rate}руб.'
                )
        else:
            bot.send_message(
                chat_id,
                'Прости, но ты ввел команду неправильно'
            )

    except CentralBankError:
        bot.send_message(
            chat_id,
            'По данной дате ничего не найдено. Вы вышли за пределы.'
        )
    except ValueError:
        bot.send_message(
            chat_id,
            'Вы ввели невалидную дату'
        )
    except IndexError:
        bot.send_message(
            chat_id,
            'Пожалуйста введите /cb *Валюты на русском языке* *ДЕНЬ-МЕСЯЦ-ГОД*'
        )


def get_currency_test(text: str):
    result = re.findall(r'доллар|евр|юан|фунт|иен|', text)
    result += re.findall(
        r'благовещенск|архангельск|астрахан|белгород|брянск|владимир|волгоград|вологд|воронеж|иванов|иркутск|'
        r'калининград|калуг|петропавловс|кемерово|киров|костром|курган|курск|санкт-петербург|липецк|магадан|'
        r'москв|мурманск|нижн|велик|новосибирск|омск|оренбург|пенз|перм|псков|ростов|рязан|самар|саратов|'
        r'южн|екатеринбург|смоленск|тамбов|тул|тюмен|ульяновск|челябинск|чит|ярославл|майкоп|горно-алтайск|'
        r'уф|улан-уде|махачкал|биробиджан|нальчик|элист|черкесск|петрозавосдск|сыктывкар|симферопол|йошкар-ол|'
        r'саранск|якутск|владикавказ|казан|кызыл|ижевск|абакан|грозн|чебоксар|барнаул|краснодар|красноярск|'
        r'владивосток|ставропол|хабаровск|нарьян-мар|ханты-мансийск|анадыр|салехард', text)
    result = list(filter(lambda a: a != '', result))

    if len(result) == 2:
        curr_url = ''
        for currency_key, currency_value in currencies.items():
            if currency_key.lower().find(result[0]) > -1:
                curr_url = currency_value
                text = currency_key + '\n'
                break

        city_url = ''
        for city_key, city_value in cities.items():
            if city_key.lower().find(result[1]) > -1:
                city_url = city_value
                text += 'г.' + city_key + '\n'
                break

        try:
            myFin = Myfin(curr_url, city_url)
            banks = myFin.get_rate()

            if len(banks) >= 5:
                banks = banks[0:5]
                for bank in banks:
                    text += f'{bank.bank_name}\nПокупка: {bank.rate_buy} руб.\n' \
                            f'Продажа: {bank.rate_sell} руб.\n\n'
            elif len(banks) == 0:
                text += 'Видимо эта валюты не присутствует в городе'
            else:
                for bank in banks:
                    text += f'{bank.bank_name}\nПокупка: {bank.rate_buy} руб.\n' \
                            f'Продажа: {bank.rate_sell} руб.\n\n'

            return text
        except MyFinBankError:
            text = 'Произошла неизвестная ошибка'
            return text
    else:
        text = 'Прости, но я ничего не нашел'
        return text


@bot.message_handler(content_types=['text'])
def do_get_curr(message):
    """
    Функция, находящая курс валюты в банках города через сайт Myfin.ru
    :param message: сообщение пользователя
    :return: информация о курсе в текущем городе
    """
    if message.chat.type == "private":
        chat_id = message.chat.id
        text = str(message.text).lower()
        bot.send_message(
            chat_id,
            get_currency_test(text)
        )

    if message.chat.type == "group":
        chat_id = message.chat.id
        text = str(message.text).lower()
        if text.find('@Currency_ITMO_bot'.lower()) > -1:
            bot.send_message(
                chat_id,
                get_currency_test(text)
            )


@bot.message_handler(content_types=["sticker"])
def do_sticker(message):
    """
    Функция, отвечающая на стикер
    :param message: сообщение пользователя
    :return: ответ на стикер
    """
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классный стикер'
        )


@bot.message_handler(content_types=["photo"])
def do_photo(message):
    """
    Функция, отвечающая на фото
    :param message: сообщение пользователя
    :return: ответ на фото
    """
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классное фото'
        )


@bot.message_handler(content_types=["audio"])
def do_audio(message):
    """
    Функция, отвечающая на аудио
    :param message: сообщение от пользователя
    :return: ответ на аудио
    """
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классное аудио'
        )


@bot.message_handler(content_types=["document"])
def do_document(message):
    """
    Функция, отвечающая на документ
    :param message: сообщение от пользователя
    :return: ответ на документ
    """
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            'Классный документ'
        )


bot.polling(none_stop=True, interval=0)
