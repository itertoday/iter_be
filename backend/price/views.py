from rest_framework import viewsets
from price.service import DefaultStrategy
from rest_framework.response import Response

class PriceViewset(viewsets.ViewSet):
    
    def create(self, request):
        # This needs total enhancements
        data = request.data.copy()
        print("input", data)
        products = data.pop('products', [])
        limit = data.pop('limits', 2)
        price = DefaultStrategy.price(products, limit)
        output = { 'status': 'OK', 'price': price}
        return Response(output)
