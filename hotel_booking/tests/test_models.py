import unittest
from django.test import TestCase
from hotel_booking.models import Room, Booking
from django.contrib.auth.models import User
from datetime import date, timedelta
from decimal import Decimal


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name="Ocean View",
            price=Decimal("150.00"),
            description="A sea-facing room.",
            available=True,
            capacity=2,
            room_type=Room.DOUBLE
        )

    def test_room_str_returns_name(self):
        self.assertEqual(str(self.room), "Ocean View")

    def test_room_defaults(self):
        self.assertTrue(self.room.available)
        self.assertEqual(self.room.capacity, 2)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.room = Room.objects.create(
            name="Suite 101",
            price=Decimal("200.00"),
            description="Suite with garden view.",
            capacity=2,
            room_type=Room.SUITE
        )
        self.booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=3),
            duration=3,
            total_cost=Decimal("600.00"),
            guests=2
        )

    def test_booking_str_representation(self):
        self.assertIn("Suite 101", str(self.booking))
        self.assertIn("testuser", str(self.booking))

    def test_booking_total_cost_is_correct(self):
        expected_cost = self.room.price * self.booking.duration
        self.assertEqual(self.booking.total_cost, expected_cost)
