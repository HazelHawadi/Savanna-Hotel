from django.test import TestCase
from django.contrib.auth.models import User
from hotel_booking.models import Room
from reviews.models import Review

class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.room = Room.objects.create(name="Test Room", description="Nice room", price=100)
        self.review = Review.objects.create(
            user=self.user,
            room=self.room,
            rating=4,
            comment="Great stay!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.user.username, "testuser")
        self.assertEqual(self.review.room.name, "Test Room")
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "Great stay!")
        self.assertIsNotNone(self.review.created_at)

    def test_review_str_method(self):
        expected_str = f"{self.user.username} - {self.room.name} ({self.review.rating} stars)"
        self.assertEqual(str(self.review), expected_str)
