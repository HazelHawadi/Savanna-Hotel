from django.test import TestCase
from django.contrib.auth.models import User
from .models import Room, Booking


class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.room = Room.objects.create(name="Deluxe Suite", price=150)

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in="2025-04-01",
            check_out="2025-04-05"
        )
        self.assertEqual(booking.room.name, "Deluxe Suite")

def test_prevent_double_booking(self):
    Booking.objects.create(room=self.room, check_in_date=date(2025, 7, 1), check_out_date=date(2025, 7, 5), user=self.user)
    form_data = {
        'check_in_date': '02/07/2025',
        'check_out_date': '06/07/2025',
        'guests': 1
    }
    form = BookingForm(data=form_data, room=self.room)
    self.assertFalse(form.is_valid())
    self.assertIn('This room is already booked', form.errors['__all__'])