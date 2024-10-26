import matplotlib.pyplot as plt

def plot_predictions(data, tomorrow_price, predicted_15_min, predicted_1_hour):
    plt.figure(figsize=(14, 7))
    plt.plot(data['timestamp'], data['close_binance'], label='Price', color='blue')  # Use 'close_binance'
    plt.plot(data['timestamp'], data['SMA'], label='SMA', color='orange')
    plt.plot(data['timestamp'], data['EMA'], label='EMA', color='green')
    plt.fill_between(data['timestamp'], data['BB_upper'], data['BB_lower'], color='gray', alpha=0.5, label='Bollinger Bands')
    
    # Display current price
    current_price = data['close_binance'].iloc[-1]
    plt.axhline(y=current_price, color='red', linestyle='--', label=f'Current Price: {current_price:.2f}')
    
    # Add predicted price lines
    plt.axhline(y=predicted_15_min, color='purple', linestyle='--', label=f'Predicted Price (15 min): {predicted_15_min:.2f}')
    plt.axhline(y=predicted_1_hour, color='orange', linestyle='--', label=f'Predicted Price (1 hour): {predicted_1_hour:.2f}')
    plt.axhline(y=tomorrow_price, color='pink', linestyle='--', label=f'Predicted Price (1 day): {tomorrow_price:.2f}')
    
    # Highlight buy/sell signals
    buy_signals = data[data['Predictions'] == 1]
    sell_signals = data[data['Predictions'] == 0]
    
    plt.scatter(buy_signals['timestamp'], buy_signals['close_binance'], marker='^', color='green', label='Buy Signal', s=100)
    plt.scatter(sell_signals['timestamp'], sell_signals['close_binance'], marker='v', color='red', label='Sell Signal', s=100)
    
    plt.title('Ethereum Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()