from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Room, Booking
from .forms import BookingForm, AddRoomForm

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

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        duration = int(request.POST['duration'])
        total_cost = room.price * duration

        booking = Booking.objects.create(
            room=room, name=name, email=email, duration=duration, total_cost=total_cost
        )
        return redirect('hotel_booking:booking_success', booking_id=booking.id)
    return render(request, 'hotel_booking/book_room.html', {'room': room})