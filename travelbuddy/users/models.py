from django.contrib.auth.models import User
from django.db import models
from destination.models import Destination

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True) 
    travel_preferences = models.TextField(blank=True) 
    travel_interests = models.TextField(blank=True) 
    users_interested = models.ManyToManyField(User, related_name='user_destination_interests')

    def __str__(self):
        return f'{self.user.username} Profile'



class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    travel_dates = models.DateField()
    users_interested = models.ManyToManyField(User, related_name='interested_destinations', blank=True)

    def __str__(self):
        return self.name



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)  # Adjust as needed
    content = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"




ACTIVITY_CHOICES = [
    ('skiing', 'Skiing'),
    ('swimming', 'Swimming'),
    ('festival', 'Festival'),
    ('hiking', 'Hiking'),
    ('dining', 'Dining Experience'),
]

class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'{self.name} at {self.place}'

class Activity(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)

    def __str__(self):
        return f'{self.get_activity_type_display()} at {self.place}'
