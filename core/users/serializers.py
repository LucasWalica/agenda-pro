from rest_framework import serializers
from .models import BusinessProfile
from django.contrib.auth.models import User

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = [
            'business_name', 'phone', 'website', 'address',
            'latitude', 'longitude', 'open_time', 'close_time', 'max_reservation_per_slot'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']