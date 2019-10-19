from django.contrib.auth.models import User
from api.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['address', 'phone']


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
