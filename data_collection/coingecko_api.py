import requests

def fetch_coingecko_data():
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    params = {"vs_currency": "usd", "days": "30"}
    response = requests.get(url, params=params)
    data = response.json()
    return [{'timestamp': item[0], 'price': item[1]} for item in data['prices']]