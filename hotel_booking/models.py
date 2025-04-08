from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from decimal import Decimal
from django import forms

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
    featured_image = CloudinaryField('image', default='placeholder')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    capacity = models.IntegerField(default=1)
    room_type = models.CharField(
        max_length=20, 
        choices=ROOM_TYPE_CHOICES, 
        default=SINGLE
    )


    def __str__(self):
        return self.name

# Booking model to define the bookings for rooms
class Booking(models.Model):
    name = models.CharField(max_length=255, default="Unknown User")
    email = models.EmailField(default='example@example.com')
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField(default=1)
    duration = models.IntegerField(default=1)
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        null=False,
        blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    CONFIRMED = 'Confirmed'
    PENDING = 'Pending'
    CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (PENDING, 'Pending'),
        (CANCELLED, 'Cancelled'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
        return f"Booking for {self.room.name} by {self.user.username if self.user else 'Guest'}"
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in_date', 'check_out_date', 'guests']
    
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            raise forms.ValidationError("Check-out date must be after check-in date.")
        
        return cleaned_data
    