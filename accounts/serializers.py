from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=13)
    profile_image = serializers.ImageField()
    profile_token = serializers.CharField(max_length=100)
    otp = serializers.CharField(max_length=20)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'profile_image', 'profile_token', 'created', 'otp')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
