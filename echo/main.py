import re
import telebot
import datetime

from echo.config import TG_TOKEN
from echo.CityNamesCurrencies import cities
from echo.CityNamesCurrencies import currencies

from apis.CbBank import CbBank
from apis.CbBank import CentralBankError

from apis.Myfin import Myfin
from apis.Myfin import MyFinBankError

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def do_start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот и мне нормально')


@bot.message_handler(commands=['help'])
def do_help(message):
    bot.send_message(
        message.chat.id,
        "Это бот\n\n" +
        "Введите предложение, в котором есть город и валюта (доллар, евро ...), чтобы узнать курс\n\n" +
        "Чтобы узнать курс в ЦБ, напишите /cb *Дата в формате день.месяц.год*\n\n" +
        "Чтобы узнать какие города поддерживаются, напишите /cities\n\n" +
        "Поддерживаются валюты: доллар, евро, фунт, иена, юань(не поддерживается в ЦБ)\n\n" +
        "Также я отвечу повотором на любое твое сообщение",
    )


@bot.message_handler(commands=['cities'])
def do_countries(message):
    text = ''
    for city in cities.keys():
        text = text + city + '\n'
    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(commands=['cb'])
def do_cb(message):
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
    except CentralBankError:
        bot.send_message(
            chat_id,
            'По данной дате ничего не найдено'
        )
    except ValueError:
        bot.send_message(
            chat_id,
            'Вы ввели невалидную дату'
        )
    except IndexError:
        bot.send_message(
            chat_id,
            'Пожалуйста введите число'
        )


@bot.message_handler(content_types=['text'])
def do_get_curr(message):
    if message.chat.type == "private":
        chat_id = message.chat.id
        text = str(message.text).lower()
        result = re.findall(r'доллар|евро|юан|фунт|иена|', text)
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
                if result[0] == currency_key.lower():
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
            except MyFinBankError:
                bot.send_message(
                    chat_id,
                    'Произошла неизвестная ошибка'
                )

            bot.send_message(
                chat_id,
                text
            )
        else:
            bot.send_message(
                chat_id,
                'Прости, но я ничего не нашел'
            )

    if message.chat.type == "group":
        chat_id = message.chat.id
        text = str(message.text).lower()
        if text.find('@Currency_ITMO_bot'.lower()) > -1:
            result = re.findall(r'доллар|евро|юан|фунт|иена|', text)
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
                    if result[0] == currency_key.lower():
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
                except MyFinBankError:
                    bot.send_message(
                        chat_id,
                        'Произошла неизвестная ошибка'
                    )

                bot.send_message(
                    chat_id,
                    text
                )
            else:
                bot.send_message(
                    chat_id,
                    'Прости, но я ничего не нашел'
                )


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
