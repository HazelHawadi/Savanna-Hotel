from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Room, Booking
from .forms import BookingForm, AddRoomForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
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

def add_room(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking:admin_home')
    else:
        form = AddRoomForm()
    return render(request, 'hotel_booking/add_room.html', {'form': form})

def room_details(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'hotel_booking/room_details.html', {'room': room})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    total_cost = None  # Initialize total_cost for GET request

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # Handle missing dates
        if not check_in_date:
            check_in_date = date.today()

        if not check_out_date:
            check_out_date = date.today()

        # Calculate the duration in days
        duration = int((date.fromisoformat(check_out_date) - date.fromisoformat(check_in_date)).days)

        # If duration is negative, set it to 1 day
        if duration < 1:
            duration = 1

        # Calculate the total cost using Decimal for correct arithmetic
        total_cost = Decimal(room.price) * Decimal(duration)

        # Create the booking
        booking = Booking.objects.create(
            room=room,
            name=request.user.get_full_name(),  # Use logged-in user's name
            email=request.user.email,  # Use logged-in user's email
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            duration=duration,
            total_cost=total_cost
        )

        return redirect('hotel_booking:room_details', room_id=room.id)

    return render(request, 'hotel_booking/book_room.html', {'room': room, 'total_cost': total_cost})
    
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