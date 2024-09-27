from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import login, profile

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    # path('destination-search/', views.destination_search, name='destination_search'),
    path('trip-planning/', views.trip_planning, name='trip_planning'),
   # path('trip_planning/', views.trip_planning_home, name='trip_planning'),
    path('trip_planning/', views.trip_planning_home, name='trip_planning'),
    path('select_accommodation/', views.select_accommodation, name='select_accommodation'),
    path('select_activity/', views.select_activity, name='select_activity'),
    path('select_place/', views.select_place, name='select_place'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/post/', views.post_review, name='post_review'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    #path('reviews/post/', views.post_review, name='post_review'),
    path('safety-privacy/', views.safety_privacy, name='safety_privacy'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
]
