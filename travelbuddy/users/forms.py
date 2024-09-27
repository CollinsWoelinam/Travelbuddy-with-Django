from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Review, Place, Accommodation, Activity

class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    profile_picture = forms.ImageField(required=False, label='Profile Picture')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile_picture = self.cleaned_data.get('profile_picture')
            profile = Profile.objects.create(user=user)
            if profile_picture:
                profile.profile_picture = profile_picture
                profile.save()
        return user



class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'travel_preferences', 'travel_interests']


class DestinationSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label='Destination Name')
    location = forms.CharField(max_length=255, required=False, label='Location')
    travel_dates = forms.DateField(required=False, label='Travel Dates', widget=forms.TextInput(attrs={'type': 'date'}))




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'})
        }





# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['title', 'content', 'rating']  # Update fields as needed


def post_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  
            review.user = request.user 
            review.save()  
            return redirect('reviews:list') 
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/post_review.html', {'form': form})




ACTIVITY_CHOICES = [
    ('skiing', 'Skiing'),
    ('swimming', 'Swimming'),
    ('festival', 'Festival'),
    ('hiking', 'Hiking'),
    ('dining', 'Dining Experience'),
]


class PlaceSelectionForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name']

class AccommodationSelectionForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['name']

class ActivitySelectionForm(forms.ModelForm):
    activity_type = forms.MultipleChoiceField(choices=ACTIVITY_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Activity
        fields = ['activity_type']

