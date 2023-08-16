from binance.client import Client
from plotly.subplots import make_subplots
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import random

# -------------------------------
# IMPORTANTE: para utilizar cualquiera de los EDA, hay que poner la API-KEY de Binance de cada uno! (Por obvias cuestiones de seguridad, yo subo los EDA sin las key)
# -------------------------------

def get_graph_by_interval(interval, symbol):

   #precio de btc en base a un intervalo de fechas:
   start_date = st.date_input("desde", pd.to_datetime('2018-01-01'), key=random.randint(0,9999999))
   end_date = st.date_input("hasta", pd.to_datetime('2023-08-16'), key=random.randint(0,9999999))
   candles = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_date.strftime('%d %b, %Y'), end_str=end_date.strftime('%d %b, %Y'))
   df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

   #conversion de timestamp en date
   df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
   df.set_index('timestamp', inplace=True)
      

   df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()
   df['MA50'] = df['close'].rolling(window=50).mean()
   df['MA200'] = df['close'].rolling(window=200).mean()
   
   fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])

   #velas japonesas
   candlestick_trace = go.Candlestick(
       x=df.index,
       open=df['open'].astype(float),
       high=df['high'].astype(float),
       low=df['low'].astype(float),
       close=df['close'].astype(float),
       name='Precios'
   )

   #agregue las medias moviles (ema 21, ma 50 y ma 200) Las medias se basan endatos 
   # historicos de precios y suavizar la variabilidad de los precios a lo largo del tiempo.

   #ema 21: La [EMA] considera los ultimos 21 precios de cierre y calcula un promedio ponderado de ellos.
   ema21 = go.Scatter(x=df.index, y=df['EMA21'], mode='lines', line=dict(color='green'), name='EMA21')

   #ma50: promedia los ultimos 50 precios de cierre y suaviza las variaciones a lo largo del tiempo.
   ma50 = go.Scatter(x=df.index, y=df['MA50'], mode='lines', line=dict(color='orange'), name='MA50')

   #ma200: se utiliza comunmente para identificar tendencias a largo plazo y señales de inversion.
   ma200 = go.Scatter(x=df.index, y=df['MA200'], mode='lines', line=dict(color='red'), name='MA200')


   fig.add_trace(candlestick_trace, row=1, col=1)
   fig.add_trace(ema21, row=1, col=1)
   fig.add_trace(ma50, row=1, col=1)
   fig.add_trace(ma200, row=1, col=1)


   #volumen: el volumen en este caso indica la cantidad de cripto operada en un rango especifico de tiempo-precio.
   #representa la "actividad"

   volume_trace = go.Bar(
       x=df.index,
       y=df['volume'].astype(float),
       marker=dict(color='blue'),
       name='Volumen'
   )

   fig.add_trace(volume_trace, row=2, col=1)

   fig.update_layout(xaxis_rangeslider_visible=False)
   st.plotly_chart(fig)


api_key = 'completar con api key de binance'
api_secret = 'completar con api secret de binance'

client = Client(api_key, api_secret)

ticker = client.get_ticker(symbol='BTCUSDT')

print(f"Precio actual de BTC: {ticker['lastPrice']} USDT")

st.title('Analisis [ Mundo Cripto ]')

bitcoin, ethereum, matic, xrp = st.tabs(["Bitcoin", "Ethereum", "Matic/Polygon", "Xrp/Riple"])
with bitcoin:
    st.title("Precio de Bitcoin")
    symbol = 'BTCUSDT'
    montly, weekly, daily = st.tabs(['M', 'W', 'D'])
    with montly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1MONTH, symbol)

    with weekly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1WEEK, symbol)

    with daily:
      get_graph_by_interval(Client.KLINE_INTERVAL_1DAY, symbol)


with ethereum:
    st.title("Precio de Ethereum")
    symbol = 'ETHUSDT'
    montly, weekly, daily = st.tabs(['M', 'W', 'D'])
    with montly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1MONTH, symbol)

    with weekly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1WEEK, symbol)

    with daily:
      get_graph_by_interval(Client.KLINE_INTERVAL_1DAY, symbol)

with matic:
    st.title("Precio de Matic")
    symbol = 'MATICUSDT'
    montly, weekly, daily = st.tabs(['M', 'W', 'D'])
    with montly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1MONTH, symbol)

    with weekly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1WEEK, symbol)

    with daily:
      get_graph_by_interval(Client.KLINE_INTERVAL_1DAY, symbol)

with xrp:
    st.title("Precio de XRP")
    symbol = 'XRPUSDT'
    montly, weekly, daily = st.tabs(['M', 'W', 'D'])
    with montly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1MONTH, symbol)

    with weekly:
      get_graph_by_interval(Client.KLINE_INTERVAL_1WEEK, symbol)

    with daily:
      get_graph_by_interval(Client.KLINE_INTERVAL_1DAY, symbol)

