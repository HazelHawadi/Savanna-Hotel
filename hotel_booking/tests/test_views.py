import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from hotel_booking.models import Room, Booking
from datetime import date, timedelta
from decimal import Decimal


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="pass")
        self.room = Room.objects.create(
            name="Test Room",
            price=Decimal("100.00"),
            description="Test Description",
            capacity=2,
            room_type=Room.SINGLE,
        )

    def test_booking_requires_login(self):
        url = reverse('hotel_booking:book_room', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_successful_booking_post(self):
        self.client.login(username="user", password="pass")
        url = reverse('hotel_booking:book_room', args=[self.room.id])
        response = self.client.post(url, {
            'room': self.room.id,
            'check_in_date': (date.today()).strftime('%d/%m/%Y'),
            'check_out_date': (date.today() + timedelta(days=2)).strftime('%d/%m/%Y'),
            'guests': 1,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.exists())

    def test_booking_confirmation_permission(self):
        self.client.login(username="user", password="pass")
        booking = Booking.objects.create(
            room=self.room,
            user=self.user,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=2),
            duration=2,
            total_cost=Decimal("200.00"),
        )
        url = reverse('hotel_booking:booking_confirmation', args=[booking.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
