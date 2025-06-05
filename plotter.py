import matplotlib.pyplot as plt

def plot_data(df, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Close'], label='Close')
    plt.plot(df['SMA20'], label='SMA 20')
    plt.plot(df['SMA50'], label='SMA 50')
    plt.scatter(df.index[df['Buy']], df['Close'][df['Buy']], marker='^', color='green', label='Buy')
    plt.scatter(df.index[df['Sell']], df['Close'][df['Sell']], marker='v', color='red', label='Sell')
    plt.title(f'{ticker} - Price & Signals')
    plt.legend()
    plt.grid()
    plt.show()
