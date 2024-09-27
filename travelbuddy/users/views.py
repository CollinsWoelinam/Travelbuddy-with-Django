from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Review, Destination
from .forms import CustomUserRegistrationForm, ProfileUpdateForm, CustomUserUpdateForm, DestinationSearchForm, ReviewForm
from .forms import PlaceSelectionForm, AccommodationSelectionForm, ActivitySelectionForm
from .models import Place, Accommodation, Activity
from django.contrib.auth import login as auth_login



#Home page
def home(request):
    return render(request, 'base.html')


#Destination
# models.py
from django.db import models
from django.contrib.auth.models import User

class DestinationView(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    travel_dates = models.DateField()

    #users_interested = models.ManyToManyField(User, related_name='interested_destinations', blank=True)

    def __str__(self):
        return self.name



#Trip_planning
def trip_planning(request):
    return render(request, 'trip_planning.html')

#Review
def reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/review.html', {'reviews': reviews})


#PostReview
def post_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review')  # Redirect to the reviews page after posting
    else:
        form = ReviewForm()
    return render(request, 'reviews/post_review.html', {'form': form})

#Safety
def safety_privacy(request):
    return render(request, 'safety_privacy.html')

# Register View
def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Redirect to the profile page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect('base')

# Profile View
@login_required
def profile(request):
    return render(request, 'profile.html')


#Update_profile
def update_profile(request):
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to profile after updating
        
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'update_profile.html', context)


    #Review_List
def review_list(request):
    reviews = Review.objects.all()  # Fetch all reviews
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def post_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new review
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/post_review.html', {'form': form})



def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Fetch users who went on the trip or have a related review
    related_reviews = Review.objects.filter(destination=review.destination)  # Adjust this based on your relationships
    
    context = {
        'review': review,
        'related_reviews': related_reviews,
    }
    return render(request, 'reviews/review_detail.html', context)



#Destination_Detail
def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    return render(request, 'destination/detail.html', {'destination': destination})


#TripPlanning

#Trip planning home
def trip_planning_home(request):
    return render(request, 'trip_planning_home.html')

def trip_planning(request):
    if request.method == 'POST':
        place_form = PlaceSelectionForm(request.POST)
        if place_form.is_valid():
            selected_place = place_form.cleaned_data['name']
            return redirect('select_accommodation', place_id=selected_place.id)
    else:
        place_form = PlaceSelectionForm()

    return render(request, 'trip_planning.html', {'place_form': place_form})

def select_accommodation(request, place_id):
    place = Place.objects.get(id=place_id)
    accommodations = Accommodation.objects.filter(place=place)

    if request.method == 'POST':
        accommodation_form = AccommodationSelectionForm(request.POST)
        if accommodation_form.is_valid():
            return redirect('select_activity', place_id=place.id)
    else:
        accommodation_form = AccommodationSelectionForm()

    return render(request, 'select_accommodation.html', {'place': place, 'accommodations': accommodations, 'form': accommodation_form})

def select_activity(request, place_id):
    place = Place.objects.get(id=place_id)
    activities = Activity.objects.filter(place=place)

    if request.method == 'POST':
        activity_form = ActivitySelectionForm(request.POST)
        if activity_form.is_valid():
            selected_activities = activity_form.cleaned_data['activity_type']
            # Process selected activities (you can save them to the database)
            return redirect('trip_summary')
    else:
        activity_form = ActivitySelectionForm()

    return render(request, 'select_activity.html', {'place': place, 'form': activity_form})


def select_accommodation(request):
    return render(request, 'select_accommodation.html')

def select_activity(request):
    return render(request, 'select_activity.html')

def select_place(request):
    return render(request, 'select_place.html')
