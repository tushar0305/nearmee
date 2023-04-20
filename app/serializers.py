from rest_framework import serializers
from accounts.models import *


class AppImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppImage
        fields = ('id', 'image', 'detail')

class UserComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComplaint
        fields = '__all__'