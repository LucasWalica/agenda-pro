from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import User, BusinessProfile
from .serializers import UserSerializer, BusinessProfileSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

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

        user = authenticate(email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token":token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
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

    #def get_queryset(self):
        # need to get all the clients from a business

class BusinessDetailView(generics.RetrieveAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = BusinessProfile.objects.all() 
    serializer_class = BusinessProfileSerializer
    lookup_field = "id"


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


class BusinessPostView(generics.CreateAPIView):
    parser_classes =  [JSONParser]
    permission_classes = [IsAuthenticated]
    queryset = BusinessProfile.objects.all() 
    serializer_class = BusinessProfileSerializer

