from django.contrib import admin
from supply.models import Transport, LocationSupply, TransportOrder

admin.site.register(Transport)
admin.site.register(LocationSupply)
admin.site.register(TransportOrder)
