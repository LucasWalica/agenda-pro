from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import BusinessProfile
from django.contrib.auth.models import User 
from .serializers import UserSerializer, BusinessProfileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from reservations.models import Reservation

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        
        if not user:
            return Response({'error':"invalid credentialds"}, status=401)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token":token.key,
            "user": {
                "id": user.id,
                    "email": user.email,
                },
            }, status=201)
    

#login 

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Importante: authenticate espera username, por eso ponemos email en username
        user = authenticate(username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                }
            }, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=401)

        

#logout 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message':"user logout succesfully"}, status=200)    


# list all the clients from a busines
class ClientListView(generics.ListAPIView): 
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all() 
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        busines = BusinessProfile.objects.filter(user=user)
        if not busines:
            return User.objects.none()
        reservations = Reservation.objects.filter(fkBusiness=busines)
        client_ids = reservations.values_list('fkClient__id', flat=True).distinct()
        clients = User.objects.filter(id__in=client_ids)
        return clients

class BusinessDetailView(generics.RetrieveAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = BusinessProfile.objects.all() 
    serializer_class = BusinessProfileSerializer
    lookup_field = "id"


# maybe add a limiter in radius via coordinates but this later
class BusinessListView(generics.ListAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = BusinessProfile.objects.all() 
    serializer_class = BusinessProfileSerializer


class BusinessUpdateView(generics.UpdateAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = BusinessProfile.objects.all() 
    serializer_class = BusinessProfileSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        user = self.request.user 
        business = self.get_object()
        if business.user != user:
            raise PermissionDenied("No tienes permido para modificar estos datos")
        return super().update(request, *args, **kwargs)
    



# por ahora solo puedes manejar un negocio
class BusinessPostView(generics.CreateAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = BusinessProfile.objects.all() 
    serializer_class = BusinessProfileSerializer

    def create(self, request, *args, **kwargs):
        user = request.user 
        busines = BusinessProfile.objects.filter(user=user)
        if busines:
            raise Exception("Ya tienes creado un negocio")
        return super().create(request, *args, **kwargs)

