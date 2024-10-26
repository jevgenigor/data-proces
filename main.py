from data_collection.binance_api import fetch_binance_data
from data_collection.coingecko_api import fetch_coingecko_data
from indicators.indicators import calculate_indicators
from model.model import train_model, predict
from visualization.visualization import plot_predictions
import pandas as pd
import numpy as np

def main():
    # Fetch data from both APIs
    binance_data = fetch_binance_data()
    coingecko_data = fetch_coingecko_data()
    
    # Convert to DataFrame
    binance_df = pd.DataFrame(binance_data)
    coingecko_df = pd.DataFrame(coingecko_data)
    
    # Rename columns in Binance DataFrame
    binance_df.rename(columns={
        'close': 'close_binance',
        'open': 'open_binance',
        'high': 'high_binance',
        'low': 'low_binance',
        'volume': 'volume_binance'
    }, inplace=True)
    
    # Rename columns in CoinGecko DataFrame
    coingecko_df.rename(columns={
        'price': 'close_coingecko'
    }, inplace=True)
    
    # Convert timestamps to datetime
    binance_df['timestamp'] = pd.to_datetime(binance_df['timestamp'], unit='ms')
    coingecko_df['timestamp'] = pd.to_datetime(coingecko_df['timestamp'], unit='ms')
    
    # Merge on timestamp
    combined_data = pd.merge_asof(binance_df.sort_values('timestamp'), 
                                   coingecko_df.sort_values('timestamp'), 
                                   on='timestamp', 
                                   direction='backward')
    
    # Print column names for debugging
    print("Combined Data Columns:", combined_data.columns)
    
    # Calculate indicators
    indicators = calculate_indicators(combined_data)
    
    # Drop rows with NaN values
    indicators.dropna(inplace=True)
    
    # Prepare features and labels for the model
    if 'close_binance' in indicators.columns:
        labels = (indicators['close_binance'].shift(-1) > indicators['close_binance']).astype(int).dropna()
    else:
        raise KeyError("Column 'close_binance' not found in indicators DataFrame.")
    
    features = indicators[['SMA', 'EMA', 'RSI', 'MACD']]
    
    # Align features and labels
    features = features[:-1]  # Drop the last row of features to match labels
    labels = labels[1:]       # Drop the first row of labels to match features
    
    # Train the model
    model = train_model(features, labels)
    
    # Make predictions
    predictions = predict(model, features)
    
    # Add predictions to the DataFrame for visualization
    indicators.loc[indicators.index[-len(predictions):], 'Predictions'] = predictions
    
    # Future price prediction using the model
    last_features = indicators[['SMA', 'EMA', 'RSI', 'MACD']].iloc[-1].values.reshape(1, -1)
    
    # Create a DataFrame for the last features
    last_features_df = pd.DataFrame(last_features, columns=['SMA', 'EMA', 'RSI', 'MACD'])
    
    # Calculate average change over the last few days
    recent_changes = indicators['close_binance'].diff().tail(5)  # Last 5 changes
    average_change = recent_changes.mean()
    
    # Predict prices for the next 15 minutes, next hour, and next day
    last_price = indicators['close_binance'].iloc[-1]
    
    # 15-Minute Prediction
    predicted_15_min = last_price + average_change * 0.25  # Assuming average change is for 1 hour
    
    # 1-Hour Prediction
    predicted_1_hour = last_price + average_change
    
    # 1-Day Prediction
    predicted_direction = model.predict(last_features_df)[0]  # 0 or 1
    if predicted_direction == 1:  # If the model predicts an increase
        predicted_1_day = last_price + average_change * 24  # Adjust for daily change
    else:  # If the model predicts a decrease
        predicted_1_day = last_price - average_change * 24  # Adjust for daily change
    
    print(f"Predicted price for the next 15 minutes: {predicted_15_min:.2f} USD")
    print(f"Predicted price for the next hour: {predicted_1_hour:.2f} USD")
    print(f"Predicted price for tomorrow: {predicted_1_day:.2f} USD")
    
    # Plot the results
    plot_predictions(indicators, predicted_1_day, predicted_15_min, predicted_1_hour)

if __name__ == "__main__":
    main()