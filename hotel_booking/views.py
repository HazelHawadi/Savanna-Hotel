from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.db import models
from .models import Room, Booking
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


# Create your views here.
logger = logging.getLogger(__name__)

# Home view for the landing page
def home(request):
    rooms = Room.objects.all()  # Fetch all rooms from the database
    return render(request, 'index.html', {'rooms': rooms})  # Render homepage template

# Home page showing all rooms
def index(request):
    rooms = Room.objects.all()  # This fetches all the rooms from the database
    return render(request, 'hotel_booking/index.html', {'rooms': rooms})

@login_required
def add_room(request):
    # Only allow staff users (admin or users with the 'can_add_room' permission)
    if not request.user.has_perm('hotel_booking.add_room'):
        messages.error(request, 'You do not have permission to add a room.')
        return redirect('hotel_booking:index')
    
    if request.method == 'POST':
        # Handle room creation logic here
        room = Room(
            name=request.POST['name'],
            price=request.POST['price'],
            description=request.POST['description'],
        )
        room.save()
        messages.success(request, 'Room added successfully!')
        return redirect('hotel_booking:index')

    return render(request, 'hotel_booking/add_room.html')

def room_details(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'room_details.html', {'room': room})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    total_cost = None  # Initialize total_cost as None for now

    if request.method == 'POST':
        # Log the POST data for debugging
        logger.debug(f"POST data received: {request.POST}")

        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Log the values of the check_in_date and check_out_date
        logger.debug(f"Check-in Date: {check_in_date}")
        logger.debug(f"Check-out Date: {check_out_date}")

        # Check if the dates are missing
        if not check_in_date or not check_out_date:
            return HttpResponseBadRequest("Check-in and check-out dates are required.")

        try:
            # Parse check-in and check-out dates safely
            check_in_date = date.fromisoformat(check_in_date)
            check_out_date = date.fromisoformat(check_out_date)

            # Calculate the duration of stay
            duration = (check_out_date - check_in_date).days
            if duration < 1:
                duration = 1  # Ensure at least one night

        except ValueError:
            return HttpResponseBadRequest("Invalid date format. Please use -MM-DDYYYY.")

        try:
            # Safely parse the price as a Decimal
            room_price = Decimal(room.price)
        except (ValueError, InvalidOperation):
            return HttpResponseBadRequest("Invalid room price.")

        # Calculate total cost
        total_cost = room_price * Decimal(duration)

        # Create the booking object
        try:
            booking = Booking.objects.create(
                room=room,
                name=request.user.get_full_name(),  # Use user's full name
                email=request.user.email,           # Use user's email
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                duration=duration,
                total_cost=total_cost,
            )

        except Exception as e:
            return HttpResponseBadRequest(f"Error creating booking: {e}")

        # Redirect to the booking confirmation page
        return redirect('hotel_booking:booking_confirmation', booking_id=booking.id)

    return render(request, 'bookings/book_room.html', {'room': room})

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('booking_success')  # Redirect after successful booking
    else:
        form = BookingForm()

    return render(request, 'create_booking.html', {'form': form})

def booking_confirmation(request, booking_id):
    # Retrieve the booking using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Pass the booking object to the template
    return render(request, 'booking_confirmation.html', {
        'booking': booking,
        'room_name': booking.room.name,
        'check_in_date': booking.check_in_date,
        'check_out_date': booking.check_out_date,
        'total_cost': booking.total_cost,
        'user_name': booking.name,
        'user_email': booking.email,
    })

# Register view

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('hotel_booking:index')  # Redirect to home page after successful registration
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
def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.user:
        messages.error(request, "You are not allowed to edit this booking.")
        return redirect('booking_list')  # Redirect to booking list

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Your booking has been updated!")
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(instance=booking)

    return render(request, 'hotel_booking/booking_form.html', {'form': form})

@login_required
def booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.user:
        messages.error(request, "You are not allowed to delete this booking.")
        return redirect('booking_list')  # Redirect to booking list

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Your booking has been deleted!")
        return redirect('booking_list')  # Redirect to booking list

    return render(request, 'hotel_booking/booking_confirm_delete.html', {'booking': booking})
