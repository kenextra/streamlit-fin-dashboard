import yfinance as yf
import streamlit as st
import datetime
import talib
import ta
import pandas as pd
# import requests
yf.pdr_override()


st.write("""
# Technical Analysis Web Application
Shown below are the **Moving Average Crossovers**, **Bollinger Bands**,
**MACD's**, **Commodity Channel Indexes**, and
**Relative Strength Indexes** of any stock!
""")

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
st_date = datetime.date(2020, 1, 1)

def user_input_features():
    ticker = st.sidebar.text_input("Ticker", "AAPL")
    # start_date = st.sidebar.text_input("Start Date", "2020-01-01")
    # end_date = st.sidebar.text_input("End Date", f'{today}')
    start_date = st.sidebar.date_input("Start Date", st_date)
    end_date = st.sidebar.date_input("End Date", today, max_value=today)
    return ticker, start_date, end_date


symbol, start, end = user_input_features()


def get_symbol(symbol):
    """
    base_url = "http://d.yimg.com/autoc.finance.yahoo.com"
    url = f"{base_url}/autoc?query={symbol}&region=1&lang=en"
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
    """
    tickerData = yf.Ticker(symbol)
    name = tickerData.info['longBusinessSummary']
    return name


company_name = get_symbol(symbol.upper())

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data
data = yf.download(symbol, start, end)

# Comapny summary
st.header(f"Company Summary\n {company_name}")

# Adjusted Close Price
st.header(f"Adjusted Close Price\n")
st.line_chart(data['Adj Close'])

# SMA and EMA
data['SMA'] = talib.SMA(data['Adj Close'], timeperiod=20)

# Exponential Moving Average
data['EMA'] = talib.EMA(data['Adj Close'], timeperiod=20)

# Plot
st.header(
    f"Simple Moving Average vs. Exponential Moving Average\n")
st.line_chart(data[['Adj Close', 'SMA', 'EMA']])

# Bollinger Bands
data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(
    data['Adj Close'], timeperiod=20)

# Plot
st.header(f"Bollinger Bands\n")
st.line_chart(data[['Adj Close', 'upper_band', 'middle_band', 'lower_band']])

# MACD (Moving Average Convergence Divergence)
data['macd'], data['macdsignal'], data['macdhist'] = talib.MACD(
    data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)

# Plot
st.header(f"Moving Average Convergence Divergence\n")
st.line_chart(data[['macd', 'macdsignal']])

# CCI (Commodity Channel Index)
cci = ta.trend.cci(data['High'], data['Low'],
                   data['Close'], window=31, constant=0.015)

# Plot
st.header(f"Commodity Channel Index\n")
st.line_chart(cci)

# RSI (Relative Strength Index)
data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)

# Plot
st.header(f"Relative Strength Index\n")
st.line_chart(data['RSI'])

# OBV (On Balance Volume)
data['OBV'] = talib.OBV(data['Adj Close'], data['Volume']) / 10**6

# Plot
st.header(f"On Balance Volume\n")
st.line_chart(data['OBV'])
