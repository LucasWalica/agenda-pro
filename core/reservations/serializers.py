from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.Serializer):
    class Meta:
        model = Reservation
        fields = [
            "fkClient", 
            "fkService", 
            "time_start", 
            "time_end", 
        ]
