from core.models import Order
import requests
from django.conf import settings
import json

def _price(requestItem):
    url = settings.PRICE_URL
    data = {
        'quantity': requestItem.quantity,
        'request_type': requestItem.request_type
    }

    raw_result = requests.post(url, json=data)
    print("received in _price: ", raw_result.status_code)
    result = json.loads(raw_result.text)
    return result # {status: OK, price: 4000}
    

def generateOrder(request):
    total = 0
    for item in request.items.all():
        partial = _price(item)
        total += partial.get('price', 0)

    order = Order(
        request=request,
        price=total,
        status=Order.PENDING 
    )
    order.save()