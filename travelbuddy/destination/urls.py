# destinations/urls.py
from django.urls import path
from . import views
from .views import destination_search, view_destination

urlpatterns = [
    path('search/', views.destination_search, name='destination_search'),
    path('<int:destination_id>/', views.view_destination, name='view_destination'),
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('reviews/', views.review_list, name='review_list'),
]
