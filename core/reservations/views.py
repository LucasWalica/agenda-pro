from django.shortcuts import render
from .serializers import ReservationSerializer
from .models import Reservation
from users.models import BusinessProfile
from offers.models import Service
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.db.models import Q

class ReservationDetailView(generics.RetrieveAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer
    lookup_field = 'id'


class ReservationClientListView(generics.ListAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        reservations = Reservation.objects.filter(fkClient=user)
        return reservations
    

class ReservationBusinessListView(generics.ListAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        busines_profile = BusinessProfile.objects.filter(user=user).first()
        if not busines_profile:
            return Reservation.objects.none()
        reservations = Reservation.objects.filter(fkBusiness=busines_profile)
        return reservations
    



class ReservationUpdateView(generics.UpdateAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        user = request.user 
        is_client = reservation.fkClient == user 
        is_business_owner = (reservation.fkService.fkBusiness.user == user)
        if not (is_client or is_business_owner):
            raise PermissionDenied("No tienes permido para modificar esta reserva")
        return super().update(request, *args, **kwargs)

class ReservationDeleteView(generics.DestroyAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all() 
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        user = request.user 
        is_client = reservation.fkClient == user 
        is_business_owner = (reservation.fkService.fkBusiness.user == user)
        if not (is_client or is_business_owner):
            raise PermissionDenied("No tienes permido para borrar esta reserva")
        return super().destroy(request, *args, **kwargs)



# Endpoint mas critico, checkear fuerte que funciona
class ReservationPostView(generics.CreateAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer 

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
    # Parse input
        fk_service_id = data.get("fkService")
        fk_business_id = data.get("fkBusiness")
        time_start = parse_datetime(data.get("time_start"))
        time_end = parse_datetime(data.get("time_end"))

        if not all([fk_service_id, fk_business_id, time_start, time_end]):
            raise ValidationError("Missing required fields")

        # Get business and its max reservation policy
        from offers.models import Service
        from users.models import BusinessProfile

        try:
            service = Service.objects.get(id=fk_service_id)
            business = BusinessProfile.objects.get(id=fk_business_id)
        except (Service.DoesNotExist, BusinessProfile.DoesNotExist):
            raise ValidationError("Invalid service or business ID")

        if service.fkBusiness.id != business.id:
            raise ValidationError("Service does not belong to this business")

        # Check for overlapping reservations
        overlapping_reservations = Reservation.objects.filter(
            fkBusiness=business,
            time_start__lt=time_end,
            time_end__gt=time_start
        ).count()

        if overlapping_reservations >= business.max_reservation_per_slot:
            raise ValidationError("Time slot is fully booked")

        # All good — save reservation
        serializer.save(fkClient=user, fkService=service, fkBusiness=business)


#another critic endpoint allows to paint a calender
class ReservationListGetEmptySpaceInBusines(generics.ListAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user

        business_id = self.request.query_params.get("business_id")
        if not business_id:
            return Reservation.objects.none()
        try:
            business_profile = BusinessProfile.objects.get(id=business_id)
        except BusinessProfile.DoesNotExist:
            return Reservation.objects.none()
        # Verifica que el usuario sea el dueño del negocio (opcional)
        if business_profile.user != user:
            return Reservation.objects.none()
        services = Service.objects.filter(fkBusiness=business_profile)

        reservations = Reservation.objects.filter(fkService__in=services)
        return reservations