from django.shortcuts import render
from .models import Service, CommentsOnService
#add comments later not MVP
from .serializers import CommentOnServiceSerializer, ServiceSerializer
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
from django.utils.timezone import now


# detail view
class ServiceDetailView(generics.RetrieveAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'



#It would be great to limit it in a rounded zone of X kms
class ServiceListView(generics.ListAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# allows to a business look at theis services
class ServiceBusinesListView(generics.ListAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        user = self.request.user 
        busines = BusinessProfile.objects.filter(user=user)
        services = Service.objects.filter(fkBusiness=busines)
        return services

# only allows a busines owner updates
class ServiceUpdateView(generics.UpdateAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        service = self.get_object()
        user = request.user 
        if service.fkBusiness.user != user:
            raise PermissionDenied("No tienes permido para modificar esta reserva")
        return super().update(request, *args, **kwargs)

class ServiceDeleteView(generics.DestroyAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        user = request.user 
        if service.fkBusiness.user != user:
            raise PermissionDenied("No tienes permido para borrar esta reserva")
        return super().destroy(request, *args, **kwargs)
    

class ServiceCreateView(generics.CreateAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    

# shows all the comments from a service
class CommentListByServiceView(generics.ListAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = CommentsOnService.objects.all()
    serializer_class = CommentOnServiceSerializer

    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        if not service_id:
            return CommentsOnService.objects.none()
        comments = CommentsOnService.objects.filter(fkService=service_id)
        return comments

# allows to post a commment
class CommentPostView(generics.CreateAPIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = CommentsOnService.objects.all()
    serializer_class = CommentOnServiceSerializer

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        service_id = data.get("fkService")

        if not service_id:
            raise ValidationError("Service ID is required")

        from reservations.models import Reservation
        from offers.models import Service

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise ValidationError("Service does not exist")

        # Verificar que el usuario tenga una reserva finalizada de ese servicio
        has_past_reservation = Reservation.objects.filter(
            fkClient=user,
            fkService=service,
            time_end__lt=now()
        ).exists()

        if not has_past_reservation:
            raise ValidationError("You can only comment on services you have received.")

        serializer.save(fkClient=user, fkService=service)