from django.shortcuts import render
get_object_or_404, redirect
from .models import Room, Booking
from .forms import BookingForm, AddRoomForm

# Create your views here.

# Home page showing all rooms
def index(request):
    rooms = Room.objects.all()
    return render(request, 'hotel_booking/index.html', {'rooms': rooms})