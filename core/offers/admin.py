from django.contrib import admin
from .models import Service, CommentsOnService
# Register your models here.
admin.site.register(Service)
admin.site.register(CommentsOnService)