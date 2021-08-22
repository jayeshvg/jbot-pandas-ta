import ccxt
import yfinance
import pandas_ta as ta
import pandas as pd
import requests


JBOT_TEST_CHAT_ID = "-1001539836622"


def send_telegram_message(chatId, message):
    response = requests.post(
        "https://api.telegram.org/<botid>/sendMessage?chat_id="+str(chatId)+"&text=" + message)


symbols = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'XRP/USDT']
tf = '1m'

exchange = ccxt.binance()


def alert_job(request):
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

        # WEBHOOK_URL = "your discord webhook url here"

        if last_row['ADX_14'] >= 25:
            if last_row['DMP_14'] > last_row['DMN_14']:
                message = f"STRONG UPTREND: The ADX is {last_row['ADX_14']:.2f}"
            if last_row['DMN_14'] > last_row['DMP_14']:
                message = f"STRONG DOWNTREND: The ADX is {last_row['ADX_14']:.2f}"

            send_telegram_message(JBOT_TEST_CHAT_ID, symbol +
                                  " on " + tf + " " + message)
            # payload = {
            #     "username": "alertbot",
            #     "content": message
            # }

            # requests.post(WEBHOOK_URL, json=payload)

        # if last_row['ADX_14'] < 25:
        #     message = f"NO TREND: The ADX is {last_row['ADX_14']:.2f}"

        #     send_telegram_message(JBOT_TEST_CHAT_ID, message)
        #     # payload = {
        #     #     "username": "alertbot",
        #     #     "content": message
        #     # }

        #     # requests.post(WEBHOOK_URL, json=payload)
