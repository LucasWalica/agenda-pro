from django.urls import path 
from .views import (
    CommentListByServiceView, CommentPostView,
    ServiceBusinesListView, ServiceCreateView, 
    ServiceDeleteView, ServiceDetailView, 
    ServiceListView, ServiceUpdateView
)


urlpatterns = [
    path("comment/list/", CommentListByServiceView.as_view() ),
    path("comment/post/", CommentPostView.as_view()),
    path('services/busines/list/', ServiceBusinesListView.as_view()),
    path('service/create/', ServiceCreateView.as_view()),
    path('service/delete/<int:id>/', ServiceDeleteView.as_view()),
    path('service/<int:id>/', ServiceDetailView.as_view()),
    path('service/list/', ServiceListView.as_view()),
    path("service/udate/<int:id>/", ServiceUpdateView.as_view())
]
