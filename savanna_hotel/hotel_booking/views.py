from django.shortcuts import render
get_object_or_404, redirect
from .models import Room, Booking
from .forms import BookingForm, AddRoomForm

# Create your views here.

# Home page showing all rooms
def index(request):
    rooms = Room.objects.all()
    return render(request, 'hotel_booking/index.html', {'rooms': rooms})

# Room details page
def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create booking
            booking = form.save(commit=False)
            booking.room = room
            booking.total_cost = room.price * booking.duration
            booking.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'hotel_booking/room_details.html', {'room': room, 'form': form})

# Add a new room (admin view)
def add_room(request):
    if request.method == 'POST':
        form = AddRoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = AddRoomForm()
    return render(request, 'hotel_booking/add_room.html', {'form': form})