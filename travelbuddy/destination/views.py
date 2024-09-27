# destinations/views.py
from django.shortcuts import render, get_object_or_404
from .models import Destination, Review
from .forms import DestinationSearchForm

# def destination_search(request):
#     form = DestinationSearchForm(request.GET or None)
#     results = None

#     if form.is_valid():
#         name = form.cleaned_data.get('name')
#         location = form.cleaned_data.get('location')
#         travel_dates = form.cleaned_data.get('travel_dates')

#         filters = {}
#         if name:
#             filters['name__icontains'] = name
#         if location:
#             filters['location__icontains'] = location
#         if travel_dates:
#             filters['travel_dates'] = travel_dates

#         results = Destination.objects.filter(**filters)

#     return render(request, 'search_results.html', {'form': form, 'results': results})


# views.py in destination app
from django.shortcuts import render
from .models import Destination
from .forms import DestinationSearchForm

def destination_search(request):
    form = DestinationSearchForm(request.GET or None)
    destinations = Destination.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            destinations = destinations.filter(name__icontains=query)  # Search by name

    context = {
        'form': form,
        'destinations': destinations,
    }
    return render(request, 'destination/destination_search.html', context)


def view_destination(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    interested_users = destination.users_interested.all()
    return render(request, 'destination_detail.html', {'destination': destination, 'interested_users': interested_users})



def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    users = destination.users.all()
    reviews = destination.reviews.all()
    context = {
        'destination': destination,
        'users': users,
        'reviews': reviews
    }
    return render(request, 'reviews/destination_detail.html', context)



def trip_planning(request):
    destinations = Destination.objects.all()
    return render(request, 'trip_planning.html', {'destinations': destinations})



# View to list reviews
def review_list(request):
    reviews = Review.objects.select_related('destination', 'user').all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

# View for detailed destination page showing all reviews and users who visited
def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    reviews = Review.objects.filter(destination=destination).select_related('user')
    return render(request, 'reviews/destination_detail.html', {
        'destination': destination,
        'reviews': reviews
    })

    