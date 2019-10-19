from django.contrib import admin
from core.models import Request, Order, Product, RequestItem

admin.site.register(Request)
admin.site.register(RequestItem)
admin.site.register(Order)
admin.site.register(Product)
