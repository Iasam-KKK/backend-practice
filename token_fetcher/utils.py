import json
from datetime import datetime
from requests import Session, Timeout, TooManyRedirects
from .models import Token

def fetch_token_data(symbol=None):
    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
    }

    session = Session()
    session.headers.update(headers)

    try:
        print(f"Fetching data from API for symbol: {symbol if symbol else 'all'}")
        response = session.get(url, params=parameters)
        print(f"API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"API Error: {response.content}")
            return None
        data = json.loads(response.text)
        tokens_data = data['data']
        print(f"Fetched {len(tokens_data)} tokens")

        if symbol:
            token_data = next((item for item in tokens_data if item['symbol'] == symbol.upper()), None)
            if not token_data:
                print(f"Token {symbol} not found in API response. Trying manual data...")
                token_data = get_manual_token_data(symbol)
            if token_data:
                print(f"Found data for {symbol}: {token_data['name']}")
                update_token_in_db(token_data)
                return token_data
            else:
                print(f"Token {symbol} not found")
                return None
        else:
            for token in tokens_data:
                update_token_in_db(token)
            return tokens_data
    except Exception as e:
        print(f"Error in fetch_token_data: {e}")
        return None

def get_manual_token_data(symbol):
    manual_data = {
        'BTC': {'id': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'quote': {'USD': {'price': 30000.0}}, 'last_updated': '2023-06-10T14:30:00Z'},
        'ETH': {'id': 1027, 'name': 'Ethereum', 'symbol': 'ETH', 'quote': {'USD': {'price': 1800.0}}, 'last_updated': '2023-06-10T14:30:00Z'},
        'BNB': {'id': 1839, 'name': 'Binance Coin', 'symbol': 'BNB', 'quote': {'USD': {'price': 250.0}}, 'last_updated': '2023-06-10T14:30:00Z'},
        'XRP': {'id': 52, 'name': 'XRP', 'symbol': 'XRP', 'quote': {'USD': {'price': 0.5}}, 'last_updated': '2023-06-10T14:30:00Z'},
        'ADA': {'id': 2010, 'name': 'Cardano', 'symbol': 'ADA', 'quote': {'USD': {'price': 0.35}}, 'last_updated': '2023-06-10T14:30:00Z'},
    }
    return manual_data.get(symbol.upper())

def update_token_in_db(token_data):
    symbol = token_data['symbol']
    name = token_data['name']
    price = token_data['quote']['USD']['price']
    last_updated = datetime.fromisoformat(token_data['last_updated'].replace('Z', '+00:00'))

    print(f"Attempting to update token: {name} ({symbol})")
    if len(symbol) > 20:
        print(f"Warning: Symbol {symbol} is longer than 20 characters!")

    token, created = Token.objects.update_or_create(
        symbol=symbol,
        defaults={
            'name': name,
            'price': price,
            'last_updated': last_updated
        }
    )
    print(f"Token {'created' if created else 'updated'}: {symbol}")