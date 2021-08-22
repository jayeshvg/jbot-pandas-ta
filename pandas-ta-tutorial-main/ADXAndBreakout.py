import base64


import ccxt
import yfinance
import pandas_ta as ta
import pandas as pd
import requests

JBOT_CHAT_ID = "-1001546947347"
JBOT_TEST_CHAT_ID = "-1001539836622"

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



def send_telegram_message(chatId, message):    
    print(message)
    response = requests.post(
        "https://api.telegram.org/bot1787709456:AAFqgAM0xZAC6Ph7FBVgs-3ZpmTVIkNkgJk/sendMessage?chat_id="+str(chatId)+"&text=" + message)


symbols = ['BTC/USDT', 'ETH/USDT']
tf = '1h'

exchange = ccxt.binance()


# def hello_pubsub(event, context):
#     """Triggered from a message on a Cloud Pub/Sub topic.
#     Args:
#          event (dict): Event payload.
#          context (google.cloud.functions.Context): Metadata for the event.
#     """

found = 0
consolidatingMessage = 'Possible Consolidation on 1H'    
breakingoutMessage = 'Possible breakouts on 1H'   
uptrendMessage = "Possible uptrend on 1H"   
downtrendMessage = "Possible downtrend on 1H"
with open('symbols.csv') as f:
    for line in f:
        eachline = line.strip().split(',')[0]
        symbol = eachline
        bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=500)
        df = pd.DataFrame(
            bars, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])

        # if is_consolidating(df, percentage=2.5):                
        #     consolidatingMessage+= "\n" + symbol

        if is_breaking_out(df):
            breakingoutMessage+= "\n" + symbol
            found = 1

        # adx = df.ta.adx()
        # macd = df.ta.macd(fast=14, slow=28)
        # rsi = df.ta.rsi()

        # df = pd.concat([df, adx, macd, rsi], axis=1)          

        # last_row = df.iloc[-1]

        # if last_row['ADX_14'] >= 25:
        #     if last_row['DMP_14'] > last_row['DMN_14']:
        #         uptrendMessage+= "\n" + symbol
        #     if last_row['DMN_14'] > last_row['DMP_14']:
        #         downtrendMessage+= "\n" + symbol

# send_telegram_message(JBOT_CHAT_ID, downtrendMessage)
# send_telegram_message(JBOT_CHAT_ID, uptrendMessage)
# send_telegram_message(JBOT_CHAT_ID, consolidatingMessage)
if(found):
    send_telegram_message(JBOT_CHAT_ID, breakingoutMessage)

    # pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    # print(pubsub_message)
