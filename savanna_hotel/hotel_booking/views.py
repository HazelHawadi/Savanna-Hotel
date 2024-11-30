from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
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

# Create your views here.

# Home view for the landing page
def home(request):
    # Fetch rooms to display on the homepage
    rooms = Room.objects.all()  
    return render(request, 'index.html', {'rooms': rooms})

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
    return render(request, 'hotel_booking/room_details.html', {'room': room})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    total_cost = None

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        if not check_in_date:
            check_in_date = date.today()
        if not check_out_date:
            check_out_date = date.today()

        # Calculate duration
        duration = int((date.fromisoformat(check_out_date) - date.fromisoformat(check_in_date)).days)
        if duration < 1:
            duration = 1

        # Calculate total cost
        total_cost = Decimal(room.price) * Decimal(duration)

        # Create booking
        booking = Booking.objects.create(
            room=room,
            name=request.user.get_full_name(),
            email=request.user.email,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            duration=duration,
            total_cost=total_cost,
        )

        # Redirect to confirmation page with booking_id
        return redirect('hotel_booking:booking_confirmation', booking_id=booking.id)

    return render(request, 'hotel_booking/book_room.html', {'room': room})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'hotel_booking/booking_confirmation.html', {'booking': booking})

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('hotel_booking:index')  # Redirect to home page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('hotel_booking:index')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')