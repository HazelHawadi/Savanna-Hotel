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
from .forms_auth import CustomUserCreationForm 
from hotel_booking import views



# Create your views here.

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
    return render(request, 'hotel_booking/room_details.html', {'room': room})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    total_cost = None

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        duration = int((date.fromisoformat(check_out_date) - date.fromisoformat(check_in_date)).days)
        if duration < 1:
            duration = 1

        total_cost = Decimal(room.price) * Decimal(duration)

        booking = Booking.objects.create(
            room=room,
            name=request.user.get_full_name(),  # Use user's full name
            email=request.user.email,           # Use user's email
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            duration=duration,
            total_cost=total_cost,
        )

        return redirect('hotel_booking:booking_confirmation', booking_id=booking.id)

    return render(request, 'hotel_booking/book_room.html', {'room': room})

def booking_confirmation(request, booking_id):
    # Retrieve the booking using the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Pass the booking object to the template
    return render(request, 'hotel_booking/booking_confirmation.html', {
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotel_booking:home')  # Redirect to home after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

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


def hotel_booking_view(request):
    return render(request, 'hotel_booking/hotel_booking.html')