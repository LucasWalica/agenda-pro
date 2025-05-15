from django.urls import path
from .views import (
    BusinessDetailView, 
    BusinessListView, 
    BusinessPostView, 
    BusinessUpdateView,
    ClientListView,
    LogoutView,
    UserCreateView
)

urlpatterns = [
    path('busines/detail/<int:id>/', BusinessDetailView.as_view()),
    path('busines/list/', BusinessListView.as_view()),
    path('busines/post/', BusinessPostView.as_view()),
    path("busines/update/", BusinessUpdateView.as_view()),
    path('busines/client/list/', ClientListView.as_view()),
    path("logout/", LogoutView.as_view()),
    path('register/', UserCreateView.as_view())
]
