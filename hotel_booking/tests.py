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
