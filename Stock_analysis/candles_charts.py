import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

# Define the path to the images folder
images_folder = 'images'

# Ensure the images folder exists
os.makedirs(images_folder, exist_ok=True)

# Function to calculate RSI
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

# Function to fetch data and plot the chart
def plot_stock_chart(symbol, filename):
    # Fetch historical data using yfinance
    data = yf.download(symbol, period="5y", interval="1d")
    
    # Calculate moving averages
    data['MA200'] = data['Close'].rolling(window=200).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    # Calculate RSI
    data['RSI'] = calculate_rsi(data, period=14)
    
    # Filter data to only the last 5 years
    recent_data = data[data.index >= (pd.Timestamp.today() - pd.DateOffset(years=5))].copy()
    
    # Prepare data for candlestick chart
    recent_data['Date'] = mdates.date2num(recent_data.index.to_pydatetime())
    ohlc = recent_data[['Date', 'Open', 'High', 'Low', 'Close']].copy()
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})

    # Plot candlestick chart
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='g', colordown='r', alpha=0.8)

    # Plot moving averages
    ax1.plot(recent_data['Date'], recent_data['MA200'], label='200-week MA', color='red')
    ax1.plot(recent_data['Date'], recent_data['MA50'], label='50-week MA', color='green')

    # Plot volume as bar chart
    ax1_volume = ax1.twinx()
    ax1_volume.bar(recent_data['Date'], recent_data['Volume'], width=0.6, color='blue', alpha=0.3, label='Volume')
    ax1_volume.set_ylabel('Volume')
    ax1_volume.legend(loc='upper right')

    # Highlight the last closing price
    last_close = recent_data['Close'].iloc[-1]
    ax1.axhline(last_close, color='purple', linestyle='--', linewidth=1, label=f'Last Close: {last_close:.2f}')
    ax1.text(recent_data['Date'].iloc[-1], last_close, f'{last_close:.2f}', color='purple', fontsize=12, verticalalignment='bottom')

    # Customize the candlestick chart
    ax1.set_title(f'{symbol} Price and Volume with 200-week MA')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend(loc='upper left')
    ax1.grid(True)
    ax1.xaxis_date()
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))

    # Plot RSI
    ax2.plot(recent_data.index, recent_data['RSI'], label='RSI', color='magenta')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper left')
    ax2.set_title(f'{symbol} RSI')
    ax2.grid(True)

    # Adjust layout to make sure elements are not overlapping
    plt.tight_layout()

    # Save the chart to the images folder
    filepath = os.path.join(images_folder, filename)
    plt.savefig(filepath)
    plt.close(fig)

# Plot charts for selected tickers
ticker_sym = ['ADANIENT','ADANIPORTS','APOLLOHOSP','ASIANPAINT','AXISBANK']

for sym in ticker_sym:
    plot_stock_chart(sym + '.NS', sym + '.png')
