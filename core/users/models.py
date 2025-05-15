from django.db import models
from django.contrib.auth.models import User 



class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    max_reservation_per_slot = models.PositiveIntegerField(default=1)

