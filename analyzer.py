import pandas as pd
import ta

def add_indicators(df):
    df['SMA20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['SMA50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    return df

def generate_signals(df):
    df['Buy'] = (df['RSI'] < 30) & (df['MACD'] > df['macc_signal'])
    df['Sell'] = (df['RSI'] > 70) & (df['MACD'] < df['MACD_signal'])
    return df
