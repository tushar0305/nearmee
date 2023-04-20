from rest_framework import serializers
from accounts.models import *


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_id', 'service_name', 'created', 'updated']


class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ['service_id', 'sub_service_id', 'sub_service_name', 'created', 'updated']


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
