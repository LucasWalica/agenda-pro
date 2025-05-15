from django.urls import path 
from .views import (
    ReservationBusinessListView, 
    ReservationClientListView, 
    ReservationDeleteView, 
    ReservationDetailView, 
    ReservationListGetEmptySpaceInBusines, 
    ReservationPostView, 
    ReservationUpdateView
    )

urlpatterns = [
    path('business/list/', ReservationBusinessListView.as_view()),
    path('client/list/', ReservationClientListView.as_view()),
    path('delete/<int:id>/', ReservationDeleteView.as_view()),
    path('detail/<int:id>/', ReservationDetailView.as_view()),
    path("update/<int:id>/", ReservationUpdateView.as_view()),
    path('post/', ReservationPostView.as_view()),
    path('list/calendar/', ReservationListGetEmptySpaceInBusines.as_view())
]

