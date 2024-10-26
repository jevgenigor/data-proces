import pandas as pd
import ta  # Technical Analysis library

def calculate_indicators(data):
    df = pd.DataFrame(data)
    
    # Use the Binance close price for indicators
    df['SMA'] = df['close_binance'].rolling(window=14).mean()
    df['EMA'] = df['close_binance'].ewm(span=14, adjust=False).mean()
    
    # Calculate RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['close_binance'], window=14).rsi()
    
    # Calculate MACD
    df['MACD'] = ta.trend.MACD(df['close_binance']).macd()
    
    # Calculate Bollinger Bands
    df['BB_upper'] = ta.volatility.BollingerBands(df['close_binance']).bollinger_hband()
    df['BB_lower'] = ta.volatility.BollingerBands(df['close_binance']).bollinger_lband()
    
    return df