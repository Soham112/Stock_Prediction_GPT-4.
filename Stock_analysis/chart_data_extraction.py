import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

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
    # Fetch historical data using yfinance, extending the period to ensure sufficient data for 200-week MA
    data = yf.download(symbol, period="10y", interval="1wk")
    
    # Calculate moving averages
    data['MA200'] = data['Close'].rolling(window=200).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    # Calculate RSI
    data['RSI'] = calculate_rsi(data, period=14)
    
    # Identify support and resistance levels
    recent_high = data['Close'].rolling(window=52).max().iloc[-1]
    recent_low = data['Close'].rolling(window=52).min().iloc[-1]
    
    # Plot the chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # Price and MA plot
    ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
    ax1.plot(data.index, data['MA200'], label='200-week MA', color='red')
    ax1.plot(data.index, data['MA50'], label='50-week MA', color='green')
    ax1.axhline(recent_high, color='purple', linestyle='--', label='Recent High')
    ax1.axhline(recent_low, color='orange', linestyle='--', label='Recent Low')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend(loc='upper left')
    
    # Volume plot
    ax1_volume = ax1.twinx()
    ax1_volume.bar(data.index, data['Volume'], label='Volume', color='gray', alpha=0.3)
    ax1_volume.set_ylabel('Volume')
    ax1_volume.legend(loc='upper right')
    
    # Highlight significant volume spikes (top 1%)
    significant_volume_threshold = data['Volume'].quantile(0.99)
    significant_volume_spikes = data[data['Volume'] > significant_volume_threshold]
    for spike in significant_volume_spikes.index:
        ax1_volume.axvline(spike, color='red', linestyle='--', alpha=0.5)
    
    # Annotations for recent significant events
    recent_events = {
        'Event 1': '2022-05-01',
        'Event 2': '2023-03-01'
    }
    for event, date in recent_events.items():
        if date in data.index:
            ax1.annotate(event, xy=(date, data['Close'][date]), xytext=(date, data['Close'][date] + 200),
                         arrowprops=dict(facecolor='black', shrink=0.05))
    
    # RSI plot
    ax2.plot(data.index, data['RSI'], label='RSI', color='magenta')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper left')
    ax2.set_title(f'{symbol} RSI')

    # Title and grid
    ax1.set_title(f'{symbol} Price and Volume with 200-week MA')
    ax1.grid(True)
    ax2.grid(True)
    
    # Save the chart to the images folder
    filepath = os.path.join(images_folder, filename)
    plt.savefig(filepath)
    # plt.show()

# Plot charts for selected tickers
ticker_sym = ['ABB', 'ADANIGREEN','AXISBANK','RELIANCE','CIPLA','ITC']

for sym in ticker_sym:
    plot_stock_chart(sym + '.NS', sym + '.png')
