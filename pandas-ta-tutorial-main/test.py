import base64


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


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    for symbol in symbols:
        bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=500)
        df = pd.DataFrame(
            bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

        adx = df.ta.adx()
        macd = df.ta.macd(fast=14, slow=28)
        rsi = df.ta.rsi()

        df = pd.concat([df, adx, macd, rsi], axis=1)

        print(df)

        last_row = df.iloc[-1]

        print(last_row)

        if last_row['ADX_14'] >= 25:
            if last_row['DMP_14'] > last_row['DMN_14']:
                message = f"STRONG UPTREND: ADX is at {last_row['ADX_14']:.2f}"
            if last_row['DMN_14'] > last_row['DMP_14']:
                message = f"STRONG DOWNTREND: ADX is at {last_row['ADX_14']:.2f}"

            send_telegram_message(JBOT_CHAT_ID, symbol +
                                  " on " + tf + " " + message)

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
