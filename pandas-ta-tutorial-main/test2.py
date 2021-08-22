import base64


import ccxt
import yfinance
import pandas_ta as ta
import pandas as pd

symbols = ['ETH/USDT']
tf = '1m'

exchange = ccxt.binance()

for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=500)
    df = pd.DataFrame(
        bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    print(df)



 # (1) Create the Strategy
Jbot = ta.Strategy(
    name="Jbot",
    ta=[     
        {"kind": "ema", "close": "OHLC4", "length": 10, "suffix": "OHLC4"},
    ]
)

# (2) Run the Strategy
df.ta.strategy(Jbot, **kwargs)

ema8_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=8) 
ema13_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=13)   
ema21_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=21)   
ema55_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=55)   
ema89_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=89)   
ema120_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=120)   
ema121_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=121)   
ema200_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=200)   
ema221_ohlc4 = ta.ema(ta.ohlc4(df["Open"], df["High"], df["Low"], df["Close"]), length=221)   

