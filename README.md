# TeleCurrencyBot
This is a bot that can find the currency exchange rate in a particular city. You just need to enter an offer that will contain the name of the currency and the name of the city. In response, the bot will give you 5 or less banks with the exchange rate for buying and selling currency.
### How to use this bot
+ Download and open telegram 
+ Add to itself in contacts of a bot named @Currency_ITMO_bot
+ Enter /start.
+ For more information about the bot, enter /help
+ To get information about the exchange rate from the Central Bank, enter " /cb *currency name* * date in the format DAY-MONTH-YEAR*"
+ Examples: "Шел я по шоссе и захотел узнать курс доллара в Казани", "/cb евро 12-02-2013"
### Project structure
Open the echo package and run main.py to enable the bot.
To run tests:
+ Download and open PyCharm
+ Clone the project
+ Go to the tests package
+ Launch cbTest.py to run Central Bank tests
+ Launch myFinTest.py to run MyFin banks tests