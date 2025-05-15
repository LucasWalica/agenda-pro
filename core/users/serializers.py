from rest_framework import serializers
from .models import User, BusinessProfile

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = [
            'business_name', 'phone', 'website', 'address',
            'latitude', 'longitude', 'open_time', 'close_time', 'max_reservation_per_slot'
        ]



class UserSerializer(serializers.ModelSerializer):
    business_profile = BusinessProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'is_active', 'is_staff', 'user_type', 'business_profile', 'client_profile']
