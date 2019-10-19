from django.contrib import admin
from core.models import Request, Order, Product, RequestItem, Sponsor

admin.site.register(Request)
admin.site.register(RequestItem)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Sponsor)