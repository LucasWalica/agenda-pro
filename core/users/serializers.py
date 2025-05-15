from rest_framework import serializers
from .models import BusinessProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = [
            'business_name', 'phone', 'website', 'address',
            'latitude', 'longitude', 'open_time', 'close_time', 'max_reservation_per_slot'
        ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return value

   
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Este nombre de usuario ya está registrado.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user