from rest_framework import serializers
from accounts.models import *

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class RegisteredPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['partner_token', 'profile_token']