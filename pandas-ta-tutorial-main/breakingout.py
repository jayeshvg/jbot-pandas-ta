import base64

import numpy as np
import ccxt
import yfinance
import pandas_ta as ta
import pandas as pd
import requests

JBOT_CHAT_ID = "-1001546947347"
JBOT_TEST_CHAT_ID = "-1001539836622"

def send_telegram_message(chatId, message):
    response = requests.post(
        "https://api.telegram.org/bot1787709456:AAFqgAM0xZAC6Ph7FBVgs-3ZpmTVIkNkgJk/sendMessage?chat_id="+str(chatId)+"&text=" + message)


symbols = ['BTC/USDT', 'ETH/USDT']
tf = '1h'

exchange = ccxt.binance()

def is_consolidating(df, percentage=2):
    recent_candlesticks = df[-15:]
    
    max_close = recent_candlesticks['Close'].max()
    min_close = recent_candlesticks['Close'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True        

    return False

def is_breaking_out(df, percentage=2.5):
    last_close = df[-1:]['Close'].values[0]

    if is_consolidating(df[:-1], percentage=percentage):
        recent_closes = df[-16:-1]

        if last_close > recent_closes['Close'].max():
            return True

    return False

consolidating = []
consolidatingMessage = 'Possible Consolidation on 1H'
breakingout =[]
breakingoutMessage = 'Possible breakouts on 1H'
# for symbol in symbols:
with open('symbols.csv') as f:
    for line in f:
        eachline = line.strip().split(',')[0]
        symbol = eachline
        bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=500)
        df = pd.DataFrame(
            bars, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])       

        if is_consolidating(df, percentage=2.5):
            consolidating.append(symbol)
            consolidatingMessage+= "\n" + symbol
            # print("{} is consolidating".format(filename))

        if is_breaking_out(df):
            breakingout.append(symbol)
            breakingoutMessage+= "\n" + symbol
            # print("{} is breaking out".format(filename))

print(consolidatingMessage)
print(breakingoutMessage)

send_telegram_message(JBOT_TEST_CHAT_ID, consolidatingMessage)
send_telegram_message(JBOT_TEST_CHAT_ID, breakingoutMessage)
