import base64

import numpy as np
import ccxt
import yfinance
import pandas_ta as ta
import pandas as pd
import requests

JBOT_CHAT_ID = "-1001546947347"
JBOT_TEST_CHAT_ID = "-1001539836622"


def isSupport(df,i):
    support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
    and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

    return support

def isResistance(df,i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
    and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

    return resistance
    
def find_levels(df):
    levels = []    
    s =  np.mean(df['High'] - df['Low'])
    
    for i in range(2, df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]
        
            if np.sum([abs(l-x) < s  for x in levels]) == 0:
                levels.append((i,l))
            print("At support")
        
        elif isResistance(df,i):
            l = df['High'][i]
        
            if np.sum([abs(l-x) < s  for x in levels]) == 0:
                levels.append((i,l))
            print("At resistance")
        
        else:
            print("Nothing here")
                
    return levels


# def send_telegram_message(chatId, message):
#     response = requests.post(
#         "https://api.telegram.org/bot1787709456:AAFqgAM0xZAC6Ph7FBVgs-3ZpmTVIkNkgJk/sendMessage?chat_id="+str(chatId)+"&text=" + message)


symbols = ['BTC/USDT', 'ETH/USDT']
tf = '15m'

exchange = ccxt.binance()


for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=500)
    df = pd.DataFrame(
        bars, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    levels = find_levels(df)
    print(levels)        

    # adx = df.ta.adx()
    # macd = df.ta.macd(fast=14, slow=28)
    # rsi = df.ta.rsi()

    # df = pd.concat([df, adx, macd, rsi], axis=1)

    # print(df)

    # last_row = df.iloc[-1]

    # print(last_row)

    # if last_row['ADX_14'] >= 25:
    #     if last_row['DMP_14'] > last_row['DMN_14']:
    #         message = f"STRONG UPTREND: ADX is at {last_row['ADX_14']:.2f}"
    #     if last_row['DMN_14'] > last_row['DMP_14']:
    #         message = f"STRONG DOWNTREND: ADX is at {last_row['ADX_14']:.2f}"

    #     send_telegram_message(JBOT_CHAT_ID, symbol +
    #                             " on " + tf + " " + message)
