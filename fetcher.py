import yfinance as yf

def fetch_data(ticker, period='6mo', interval='1d'):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
    return df
