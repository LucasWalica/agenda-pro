
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/offers/", include("offers.urls")),
    path("api/reservations/", include("reservations.urls")),
    path("api/users/", include("users.urls"))
]
