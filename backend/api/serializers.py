from django.contrib.auth.models import User
from api.models import Profile
from core.models import Request, RequestItem, Order, Sponsor, Product
from core.service import generateOrder
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['address', 'phone']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'sponsor', 'image_url', 'product_type')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        profile.address = profile_data.get('address', profile.address)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.save()
        return instance


class RequestItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestItem
        fields = ('id', 'quantity', 'product')
        depth = 2


class RequestItemWriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestItem
        fields = ('id', 'quantity', 'product')
        

class RequestSerializer(serializers.ModelSerializer):

    items = RequestItemSerializer(many=True)
    user  = UserSerializer(many=False)

    class Meta:
        model = Request
        fields = ('start_date', 'end_date', 'repeat', 'user', 'address', 'address2', 'city', 'items')
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    request = RequestSerializer(many=False)
    # if a transport accept, find the way to display it here

    class Meta:
        model = Order
        fields = ('request', 'price', 'status')


class RequestWriterSerializer(serializers.ModelSerializer):
    items = RequestItemWriterSerializer(many=True)

    class Meta:
        model = Request
        fields = ('start_date', 'end_date', 'repeat', 'user', 'address', 'address2', 'city', 'items')

    def create(self, validated_data):
        ''' Saving the items requested '''
        params = validated_data.copy()
        items = params.pop('items')
        request = Request(**params)
        request.update_lat_lon()
        request.save() 
        for elem in items:
            reqItem = RequestItem(**elem)
            reqItem.request = request
            reqItem.save()
        generateOrder(request) # Not sure if this goes here.
        return request
