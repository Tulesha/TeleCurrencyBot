from datetime import datetime


def log_message(message):
    file = open("logger.log", "a")
    file.write('<=====================================================>\n')
    file.write(datetime.now().strftime("%d-%m-%Y: %H-%M-%S\n"))
    file.write(f'Message from {message.from_user.last_name}, id = {message.from_user.id}\n{message.text}\n')
    file.write('>=====================================================<\n')
    file.close()


def log_exceptions(exception):
    file = open("logger.log", "a")
    file.write('<=====================================================>\n')
    file.write(f'[EXCEPTION] {type(exception).__name__}: {exception}\n')
    file.write('>=====================================================<\n')
    file.close()
