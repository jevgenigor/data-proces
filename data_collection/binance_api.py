import requests

def fetch_binance_data(symbol='ETHUSDT', interval='1h', limit=100):
    url = f'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    return [{'timestamp': item[0], 'open': float(item[1]), 'high': float(item[2]), 
             'low': float(item[3]), 'close': float(item[4]), 'volume': float(item[5])} for item in data]