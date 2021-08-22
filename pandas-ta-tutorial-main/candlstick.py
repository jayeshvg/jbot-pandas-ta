import base64

import talib
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


symbols = ['BTC/USDT']


exchange = ccxt.binance()

tf = '1h'
for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=10)
    df = pd.DataFrame(
        bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    print(df)
    engulfing = talib.CDLENGULFING(
        df['open'], df['high'], df['low'], df['close'])

    # print(num)

    df['engulfing'] = engulfing
    print(df)

    engulfing_hours = df[df['engulfing'] != 0]
    print(engulfing_hours)
   

    # if last_row['ADX_14'] >= 25:
    #     if last_row['DMP_14'] > last_row['DMN_14']:
    #         message = f"STRONG UPTREND: ADX is at {last_row['ADX_14']:.2f}"
    #     if last_row['DMN_14'] > last_row['DMP_14']:
    #         message = f"STRONG DOWNTREND: ADX is at {last_row['ADX_14']:.2f}"

    #     send_telegram_message(JBOT_CHAT_ID, symbol +
    #                           " on " + tf + " " + message)
