from rest_framework import viewsets
from price.service import DefaultStrategy
from rest_framework.response import Response

class PriceViewset(viewsets.ViewSet):
    
    def create(self, request):
        # This needs total enhancements
        data = request.data.copy()
        print("input", data)
        quantity = data.pop('quantity', 0)
        price = DefaultStrategy.price(quantity, **data)
        output = { 'status': 'OK', 'price': price}
        print("output", output)
        return Response(output)
