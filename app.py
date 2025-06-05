from flask import Flask, render_template, request, flash
import yfinance as yf
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

def fetch_data(ticker, period='6mo', interval='1d'):
    try:
        df = yf.download(ticker, period=period, interval=interval)
        if df.empty:
            return pd.DataFrame()
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def add_indicators(df):
    if df.empty:
        return df

    # Simple Moving Averages
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()

    # RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Std'] = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (2 * df['BB_Std'])
    df['BB_Lower'] = df['BB_Middle'] - (2 * df['BB_Std'])

    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    ticker = 'AAPL'
    period = '6mo'
    interval = '1d'
    data = None
    plot_data = {}
    indicators_data = {}
    recommendation = None

    if request.method == 'POST':
        ticker = request.form.get('ticker', 'AAPL').upper()
        period = request.form.get('period', '6mo')
        interval = request.form.get('interval', '1d')

    df = fetch_data(ticker, period, interval)

    if df.empty:
        flash('No data found for the given ticker/parameters.', 'danger')
    else:
        df = add_indicators(df)

        # Prepare data table
        data = df[['Date', 'Close', 'SMA20', 'SMA50', 'RSI', 'BB_Upper', 'BB_Lower', 'MACD', 'Signal']].tail(20)

        # Prepare charting data
        plot_df = df[['Date', 'Close', 'SMA20', 'SMA50', 'BB_Upper', 'BB_Lower']].tail(100).copy()
        plot_df['Date'] = pd.to_datetime(plot_df['Date']).dt.strftime('%Y-%m-%d')
        plot_data = plot_df.to_dict(orient='list')

        # Prepare indicators data
        recent_df = df.tail(100).copy()
        dates = pd.to_datetime(recent_df['Date']).dt.strftime('%Y-%m-%d')

        indicators_data = {
            'RSI': recent_df['RSI'].values.tolist(),
            'MACD': recent_df['MACD'].values.tolist(),
            'Signal': recent_df['Signal'].values.tolist(),
            'Volume': recent_df['Volume'].values.tolist(),
            'Dates': dates.values.tolist()
        }

        # Buy/Sell Recommendation
        try:
            latest = df.iloc[-1]
            if latest['RSI'] < 30 and latest['MACD'] > latest['Signal']:
                recommendation = 'BUY (RSI low & MACD bullish)'
            elif latest['RSI'] > 70 and latest['MACD'] < latest['Signal']:
                recommendation = 'SELL (RSI high & MACD bearish)'
            elif latest['Close'] > latest['SMA20'] and latest['MACD'] > latest['Signal']:
                recommendation = 'BUY (Above SMA20 & MACD bullish)'
            elif latest['Close'] < latest['SMA20'] and latest['MACD'] < latest['Signal']:
                recommendation = 'SELL (Below SMA20 & MACD bearish)'
            else:
                recommendation = 'HOLD (No strong signal)'
        except Exception as e:
            print("Error generating recommendation:", e)
            recommendation = 'Signal unavailable'

    return render_template('index.html',
                           ticker=ticker,
                           period=period,
                           interval=interval,
                           data=data,
                           plot_data=plot_data,
                           indicators_data=indicators_data,
                           recommendation=recommendation)

if __name__ == '__main__':
    app.run(debug=True)
