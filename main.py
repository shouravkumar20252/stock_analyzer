from fetcher import fetch_data
from analyzer import add_indicators, generate_signals

def analyze(ticker):
    df = fetch_data(ticker)
    df = add_indicators(df)
    df = generate_signals(df)

    print(df[['Close', 'RSI', 'MACD', 'MACD_signal', 'Buy', 'Sell']].tail(15))

    buys = df[df['Buy']]
    sells = df[df['Sell']]

    print(f"\nBuy signals for {ticker}:")
    print(buys[['Close', 'RSI', 'MACD', 'MACD_signal']])
    
    print(f"\nSell signals for {ticker}:")
    print(sells[['Close', 'RSI', 'MACD', 'MACD_signal']])

if __name__ == "__main__":
    analyze('AAPL')  # Change ticker or period in fetcher.py if you want
