import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.db import models
from .models import Room, Booking
from hotel_booking.models import Booking
from .forms import BookingForm, AddRoomForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib import messages
from datetime import date
from decimal import Decimal
from .forms_auth import CustomUserCreationForm 
from hotel_booking import views
from django.contrib.auth import logout
import logging
from .forms import BookingForm
from .forms import BookingUpdateForm


# Create your views here.
logger = logging.getLogger(__name__)

# Home view for the landing page
def home(request):
    rooms = Room.objects.all()
    for room in rooms:
        if room.featured_image:
            room.image_filename = room.featured_image.url
        else:
            room.image_filename = None  # Handle case where there's no image
    return render(request, 'index.html', {'rooms': rooms})

# Home page showing all rooms
def index(request):
    rooms = Room.objects.all()
    for room in rooms:
        if room.featured_image:
            room.image_filename = room.featured_image.url
        else:
            room.image_filename = None
    return render(request, 'hotel_booking/index.html', {'rooms': rooms})

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added successfully!")
            return redirect('hotel_booking:room_list')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = RoomForm()

    return render(request, 'hotel_booking/add_room.html', {'form': form})

def room_details(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'room_details.html', {'room': room})


def check_room_availability(room, check_in, check_out):
    # Checks if there are any bookings for the room within the date range
    bookings = Booking.objects.filter(room=room, check_in_date__lt=check_out, check_out_date__gt=check_in)
    return bookings.exists()


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Calculate total cost here
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            duration = (check_out - check_in).days
            total_cost = room.price * duration

            # Save the booking with the calculated total cost
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.duration = duration  # Save duration
            booking.total_cost = total_cost  # Save total cost
            booking.save()

            messages.success(request, "Booking confirmed!")
            return redirect('hotel_booking:booking_confirmation', booking_id=booking.id)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = BookingForm()

    return render(request, 'hotel_booking/book_room.html', {'form': form, 'room': room})

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('hotel_booking:booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'hotel_booking/create_booking.html', {'form': form})

def booking_confirmation(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)
        return render(request, 'hotel_booking/booking_confirmation.html', {'booking': booking})
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('hotel_booking:index')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful! Welcome.")
            return redirect('hotel_booking:index')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

# Custom login view
def custom_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("hotel_booking:index")

    return render(request, "registration/login.html", {"form": form})

def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')


def hotel_booking_view(request):
    return render(request, 'hotel_booking.html')


@login_required
def update_booking(request, id):
    # Retrieve the booking object by ID
    booking = get_object_or_404(Booking, id=id)
    
    if request.method == 'POST':
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            check_in = form.cleaned_data['check_in_date']
            check_out = form.cleaned_data['check_out_date']
            duration = (check_out - check_in).days
            total_cost = booking.room.price * duration

            booking = form.save(commit=False)
            booking.total_cost = total_cost
            booking.save()

            return redirect('accounts:my_bookings')
    else:
        form = BookingUpdateForm(instance=booking)

    return render(request, 'hotel_booking/booking_form.html', {'form': form, 'booking': booking})

@login_required
def my_bookings(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = []

    return render(request, 'accounts/my_bookings.html', {'bookings': bookings})

def delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    
    if request.method == 'POST':
        booking.delete()
        return redirect('accounts:my_bookings')
    
    return render(request, 'hotel_booking/confirm_delete.html', {'booking': booking})


def custom_404(request, exception):
    return render(request, '404.html', status=404)