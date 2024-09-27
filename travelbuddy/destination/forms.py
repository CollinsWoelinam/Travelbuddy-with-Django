# destinations/forms.py
from django import forms

class DestinationSearchForm(forms.Form):
    # name = forms.CharField(required=False, max_length=255)
    # location = forms.CharField(required=False, max_length=255)
    # travel_dates = forms.DateField(required=False)

    query = forms.CharField(max_length=100, required=False, label='Search Destinations')