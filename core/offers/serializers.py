from rest_framework import serializers
from .models import CommentsOnService, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["fkBusiness", "name", "price",  "description","duration"]
    


class CommentOnServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsOnService
        fields =  [ "fkClient", "fkService",  "desc",  "stars"]