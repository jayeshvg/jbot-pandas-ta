import ccxt
import pandas as pd
import requests

from datetime import datetime, time

JBOT_TEST_CHAT_ID = ""

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def send_telegram_message(chatId, message):
    response = requests.post(
        "https://api.telegram.org/<botid>/sendMessage?chat_id="+str(chatId)+"&text=" + message)


exchange = ccxt.binance()

if(is_time_between(time(12,00), time(13,00))):
    message = ''
    bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1d', limit=2)
    df = pd.DataFrame(
        bars, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])

    allHighs = df['High']
    minimum, maximum = 42000, 45000
    if(all(high >= minimum and high < maximum for high in allHighs)):
        message = "When 50k?"       

    else:
        message = "Here we go.. 50k"

    print(message)
    send_telegram_message(JBOT_TEST_CHAT_ID, message)
