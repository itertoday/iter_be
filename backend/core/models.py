from django.db import models
from django.contrib.auth.models import User
from backend import geolocator
import time
from geopy.distance import vincenty as distance # TODO: Should wrap this into some sort of abstraction

from supply.models import TransportOrder, LocationSupply, Transport
from operator import itemgetter


class Sponsor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class Product(models.Model):
    NEW_PRODUCT_TYPE = 'Nuevo'
    RELOAD_PRODUCT_TYPE = 'Recarga'

    PRODUCT_TYPE = (
        (NEW_PRODUCT_TYPE, "New"),
        (RELOAD_PRODUCT_TYPE, "Reload"),
    )
    name = models.CharField(max_length=50)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, null=True)
    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE)
    image_url = models.ImageField(upload_to='static')
    
    def __str__(self):
        return "{} ({})".format(self.name, self.product_type)


class Request(models.Model):
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField()# TODO: Add date range validation
    repeat   = models.BooleanField(default=False)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    # This can go in a seperate class
    address = models.CharField(max_length=1024, blank=False, null=False)
    address2 = models.CharField(max_length=1024, blank= True, null=True)
    city = models.CharField(max_length= 1024, blank=True, null=True)
    latitude = models.DecimalField(decimal_places=15, max_digits=18)
    longitude = models.DecimalField(decimal_places=15, max_digits=18)

    def update_lat_lon(self):
        address = geolocator.geocode(self.address)
        print("FOUND: {}".format(address))
        time.sleep(5)
        if address:
            self.latitude = address.latitude
            self.longitude = address.longitude
        else:
            self.latitude = 0.0
            self.longitude = 0.0

    @property
    def coordinate(self):
        return (self.latitude, self.longitude)
    
    def __str__(self):
        return "<Request: {}>".format(self.id)


class RequestItem(models.Model):
    

    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        # return "Item: {} - {} - {}".format(self.quantity, self.product)
        return str(self.id)


class Order(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    IN_TRANSIT = 'in transit'
    SHIPPED = 'shipped'
    CANCELLED = 'cancelled'

    STATUS = (
        (PENDING, PENDING),
        (SHIPPED, SHIPPED),
        (CANCELLED, CANCELLED),
        (ACCEPTED, ACCEPTED),
        (IN_TRANSIT, IN_TRANSIT),
    )
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request")
    price = models.DecimalField(decimal_places=5, max_digits=10) # Calculated by price app endpoint
    status = models.CharField(max_length=20, choices=STATUS)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        
        # Logic that match the order with the closest transporter
        # Ok this is kind of the heart of this app
        # This will ask for an early refactor
        # Done this way only for demo purposes
        # It is heavy
        if self.status == self.PENDING:
            print("PENDIIIING")
            # request_coord = self.request.coordinate
            # distances = [] # This will store all distances from request and available destinations
            # transport_winner = None
            # # This can be more compact
            # for _location in LocationSupply.objects.all():
            #     dist = distance(request_coord, _location.coordinate).km
            #     distances.append((_location, dist))

            # location_winner = min(distances, key=itemgetter(1))[0]

            # #Fetch correct transport
            # for tp in Transport.objects.all():
            #     transport_winner = tp if location_winner in tp.locations.all() else None

            # TransportOrder.objects.create(transport=transport_winner, order=self)

    def __str__(self):
        return "Order: {}".format(self.id)
