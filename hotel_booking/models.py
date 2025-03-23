from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Room model to define the rooms available in the hotel
class Room(models.Model):
    SINGLE = 'Single'
    DOUBLE = 'Double'
    SUITE = 'Suite'
    KING = 'King'
    QUEEN = 'Queen'
    DELUXE = 'Deluxe'
    PENTHOUSE = 'Penthouse'

    ROOM_TYPE_CHOICES = [
        (SINGLE, 'Single Room'),
        (DOUBLE, 'Double Room'),
        (SUITE, 'Suite'),
        (KING, 'King Room'),
        (QUEEN, 'Queen Room'),
        (DELUXE, 'Deluxe Room'),
        (PENTHOUSE, 'Penthouse'),
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    room_type = models.CharField(
        max_length=20, 
        choices=ROOM_TYPE_CHOICES, 
        default=SINGLE
    )


    def __str__(self):
        return self.name

# Booking model to define the bookings for rooms
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=1)
    name = models.CharField(max_length=255, default="Unknown User")
    email = models.EmailField(default='example@example.com')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True) 
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    duration = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Booking for {self.user} in {self.room} from {self.check_in_date} to {self.check_out_date}"