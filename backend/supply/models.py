from django.db import models
from django.contrib.auth.models import User
from backend import geolocator
import time


class LocationSupply(models.Model):
    location = models.CharField(max_length=1024)
    latitude = models.DecimalField(decimal_places=15, max_digits=18)
    longitude = models.DecimalField(decimal_places=15, max_digits=18)

    def __str__(self):
        return self.location

    @property
    def coordinate(self): # This is repeated in core module, think of a mixin adding latitude and longitude, maybe CoordinateMixin
        return (self.latitude, self.longitude)

    @staticmethod
    def load():
        for zone in  LocationSupply.objects.all():
            address = geolocator.geocode(zone.location)
            time.sleep(5)
            zone.latitude = address.latitude
            zone.longitude = address.longitude
            zone.save()


class Transport(models.Model):
    DRY_VAN = 'dry van'
    FLATBED = 'flatbed'
    OTHER    = 'other'

    TRANSPORT_TYPE = (
        (DRY_VAN, 'Dry Van'),
        (FLATBED, 'Flatbed'),
        (OTHER, 'Otro'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=100, choices = TRANSPORT_TYPE)
    description = models.CharField(max_length=140)
    capacity = models.PositiveIntegerField()
    locations = models.ManyToManyField(LocationSupply)

    def __str__(self):
        return "Transport: {}/{}".format(self.vehicle_type, self.owner.email)

class TransportOrder(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    order = models.ForeignKey("core.Order", on_delete=models.CASCADE) # TODO: totally illegal, as this is going to be a microservice, this should copy the Order model fields

    def __str__(self):
        return "{} - Order {}".format(self.transport, self.order)

    def save(self, *args, **kwargs):
        super(TransportOrder, self).save(*args, **kwargs)
        #This should be an endpoint call, in order to update the order
        self.order.status = self.order.ACCEPTED
        self.order.save()