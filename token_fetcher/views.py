from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Token
from .utils import fetch_token_data, get_manual_token_data, update_token_in_db

class TokenView(APIView):
    def get(self, request, symbol=None):
        if symbol:
            token_data = fetch_token_data(symbol)
            if token_data:
                data = {
                    'name': token_data['name'],
                    'symbol': token_data['symbol'],
                    'price': token_data['quote']['USD']['price'],
                    'last_updated': token_data['last_updated']
                }
                return Response(data)
            else:
                return Response({'error': f'Token with symbol {symbol} not found'}, status=404)
        else:
            tokens_data = fetch_token_data()
            if tokens_data:
                tokens = Token.objects.all()
                data = [{
                    'name': token.name,
                    'symbol': token.symbol,
                    'price': float(token.price),
                    'last_updated': token.last_updated.isoformat()
                } for token in tokens]
                return Response(data)
            else:
                # If API fails, use manual data for popular tokens
                popular_tokens = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA']
                data = []
                for symbol in popular_tokens:
                    token_data = get_manual_token_data(symbol)
                    if token_data:
                        update_token_in_db(token_data)
                        data.append({
                            'name': token_data['name'],
                            'symbol': token_data['symbol'],
                            'price': token_data['quote']['USD']['price'],
                            'last_updated': token_data['last_updated']
                        })
                return Response(data)